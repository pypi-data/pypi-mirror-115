import numpy as np
import typing as tp
import warnings

from .calculate_metrics import CalculateMetrics
from sklearn.preprocessing import normalize

representations = tp.Tuple[tp.Optional[np.ndarray], list]


class CalculateAnalogy(CalculateMetrics):
    """
    This class calculates the Accuracy of the ability of an embedding to
    perform an analogy.

    Given two pairs of words that share a relation, the analogy task of a
    embedding is to infer a fourth word (of the pair) based on the other three.

    Example: "man is to woman as king is to - ?" Pairs : (man, king),
    (woman, queen).

    This class use two different metrics to solve the analogy. They are
    3CosAdd and 3CosMul.

    The metrics used in this class are found in paper:
    Levy, O. and Goldberg, Y.: Linguistic Regularities in Sparse and Explicit
    Word Representations. 2014

    Attributes:
    :files_vocab (tp.Dict[str, list]) - a dictionary with vocabulary

    Methods:
    :get_metrics - Return the Accuracy of the 3CosAdd and 3CosMul
    """

    def __init__(self, files_vocab: tp.Dict[str, list]):
        """Initializes the class setting the file vocabulary

        :param files_vocab: Dictionary with the file vocabulary.
        :type files_vocab: `tp.Dict[str, list]`
        """
        super().__init__(files_vocab)
        self.__files_rows = files_vocab

    @staticmethod
    def calculate_3cos_add(true_word: int, col_idx: list,
                           reduced_matrix: np.ndarray) -> int:
        """Check if the word of 3CosAdd is the right word

        :param true_word: Index of the right word
        :type true_word: `int`
        :param col_idx: Original indexes of the similarity matrix
        :type col_idx: `list
        :param reduced_matrix: Matrix with the similarities of the candidates
        :type  reduced_matrix: `np.ndarray`
        :return: If the max 3CosAdd is the right word
        :rtype: int
        """
        copy_matrix = reduced_matrix.copy()
        copy_matrix[0, :] = -copy_matrix[0, :]
        cos_add = copy_matrix.sum(axis=0)
        order_idx = [i for _, i in sorted(zip(cos_add, col_idx), reverse=True)]
        return int(order_idx[0] == true_word)

    @staticmethod
    def calculate_3cos_mul(true_word: int, col_idx: list,
                           reduced_matrix: np.ndarray) -> int:
        """Check if the word of 3CosMul is the right word

        :param true_word: Index of the right word
        :type true_word: `int`
        :param col_idx: Original indexes of the similarity matrix
        :type col_idx: `list
        :param reduced_matrix: Matrix with the similarities of the candidates
        :type  reduced_matrix: `np.ndarray`
        :return: If the max 3CosMul is the right word
        :rtype: int
        """
        copy_matrix = reduced_matrix.copy()
        copy_matrix[0, :] = 1 / (copy_matrix[0, :] + 0.0001)
        cos_mul = copy_matrix[2, :] * copy_matrix[1, :] * copy_matrix[0, :]
        order_idx = [i for _, i in sorted(zip(cos_mul, col_idx), reverse=True)]
        return int(order_idx[0] == true_word)

    def __calculate_cos_metric(self, vocabulary: list, row: list,
                               similarity_matrix: np.ndarray) -> \
            tp.Tuple[int, int]:
        """ Calculate the cosine metrics for a row

        :param vocabulary: A list with the file vocabulary
        :type vocabulary: `list`
        :param row: A list with the words in a row
        :type row: `list`
        :param similarity_matrix: Matrix with the similarities of the words
        :type similarity_matrix: `np.ndarray`
        :return: The metrics for the row
        :rtype: `tp.Tuple[int, int]`
        """
        index_words = [vocabulary.index(word) for word in row]
        pair_index = [index_words[0:2], index_words[2:]]

        analogy_index = [(0, 0), (0, 1), (1, 0), (1, 1)]
        result_add = 0
        result_mul = 0
        for idx in analogy_index:
            true_word = pair_index[idx[0]][idx[1]]
            word_1 = pair_index[1 - idx[0]][1 - idx[1]]
            word_2 = pair_index[1 - idx[0]][idx[1]]
            word_3 = pair_index[idx[0]][1 - idx[1]]

            row_idx = np.array([word_1, word_2, word_3])

            col_idx = [i for i in range(similarity_matrix.shape[0])
                       if i not in row_idx]
            reduced_matrix = similarity_matrix[row_idx[:, None], col_idx]
            result_add += self.calculate_3cos_add(true_word, col_idx,
                                                  reduced_matrix)
            result_mul += self.calculate_3cos_mul(true_word, col_idx,
                                                  reduced_matrix)
        return result_add, result_mul

    def _get_representation(self, embedding: tp.Any, file: str,
                            vocab: tp.Optional[
                                list] = None) -> representations:
        """Get the embedding representation of a vocabulary

        :param embedding: Embedding model used in the analysis.
        :type embedding: `tp.Any`
        :param file: Name of the file to be analysed.
        :type file: `str`
        :param vocab: Embedding vocabulary to remove oov
        :type vocab: `tp.Optional[list]`
        :return: Array of the representations and the vocabulary used
        :rtype: `tp.Tuple[tp.Optional[np.ndarray], list]`
        """
        if vocab:
            vocabulary_dict = self._remove_out_of_vocabulary(vocab, file)
        else:
            vocabulary_dict = self._dict_vocab[file]
        if len(vocabulary_dict) == 0:
            warnings.warn(f'File {file} has no embedding representation')
            return None, vocabulary_dict
        return normalize(embedding[vocabulary_dict],
                         norm='l2'), vocabulary_dict

    def get_metrics(self, embedding: tp.Any, file: str,
                    vocab_embedding: tp.Optional[list] = None) -> \
            tp.Tuple[dict, float]:
        """Get analogy metrics of a file

        :param embedding: Embedding model used in the analysis
        :type embedding: `tp.Any`
        :param file: Name of the file to be analysed
        :type file: `str`
        :param vocab_embedding: Embedding vocabulary to remove oov
        :type vocab_embedding: `tp.Optional[list]`
        :return: Dictionary with the metrics of analogy, if the file vocabulary
        is filled with oov the metric is returned with NaN
        :rtype: `dict`
        """

        similarity_matrix, vocab_eval = self._get_cosine_matrix(embedding,
                                                                file,
                                                                vocab_embedding
                                                                )
        if len(vocab_eval) == 0:
            return {'CosAdd': np.nan, 'CosMul': np.nan}, 0

        metrics_dict = {'CosAdd': 0, 'CosMul': 0}

        number_words = 0

        for row in self.__files_rows[file]:
            if all(word in vocab_eval for word in row):
                cos_add, cos_mul = self.__calculate_cos_metric(
                    vocab_eval,
                    row,
                    similarity_matrix)

                metrics_dict['CosAdd'] += cos_add
                metrics_dict['CosMul'] += cos_mul
                number_words += 4

        if number_words == 0:
            return {'CosAdd': np.nan, 'CosMul': np.nan}, 0

        metrics_dict['CosAdd'] = metrics_dict['CosAdd'] / number_words
        metrics_dict['CosMul'] = metrics_dict['CosMul'] / number_words

        return metrics_dict, number_words
