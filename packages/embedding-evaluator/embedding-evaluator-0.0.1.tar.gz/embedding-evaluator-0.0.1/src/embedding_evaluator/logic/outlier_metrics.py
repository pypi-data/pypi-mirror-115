import numpy as np
import typing as tp

from embedding_evaluator.logic.calculate_metrics import CalculateMetrics


class OutlierMetrics(CalculateMetrics):
    """Represents outlier calculation metrics
    
    This class calculates the Accuracy and Outlier Position Percentage (OPP)
    for a given file. The previous metrics are defined as:
        * Accuracy - percentage of detected outliers
        * OPP - percentage of the outlier position according to the compactness
         score

    The calculated metrics are the following:
        * OP - Outlier Position - is defined as the position of the outlier
        according to the compactness score
        * OD - Outlier Detection - is defined as 1 if the outlier is correctly
        detected and 0 otherwise

    The outlier metrics calculated in this class are found in paper:
    Collados, J.C. and Navigli, R.: Find the word that does not belong:
    A Framework for an Intrinsic Evaluation of Word Vector Representations
    (2016)

    Attributes:
    :files_vocab (tp.Dict[str, list]) - a dictionary with vocabulary
    
    Methods:
    :get_metrics - Return the Accuracy and OPP metrics
    :calculate_op_od - Return the OP and OD
    :calculate_compactness_score - Return pseudo-inverted compactness score
    """

    def __init__(self, files_vocab: tp.Dict[str, list]):
        """Initializes the class setting the file vocabulary
        
        :param files_vocab: Dictionary with the file vocabulary.
        :type files_vocab: dict
        """
        super().__init__(files_vocab)
        self._files_vocab = files_vocab
        self._cluster_size = 8
        self._outliers_size = 8

    def get_metrics(self, embedding: tp.Any, file: str,
                    vocab_embedding: tp.Optional[list] = None) -> \
            tp.Tuple[dict, float]:
        """Get outlier metrics of a file

        :param embedding: embedding used to calculate outlier metrics
        :type embedding: `tp.Any`
        :param file: File name to evaluate
        :type file: `str`
        :param vocab_embedding: vocabulary of the embedding
        :type vocab_embedding: `tp.Optional[list]`
        :return: Dictionary containing metrics of outlier detection
        :rtype: `tp.Tuple[dict, float]`
        """
        similarity_matrix, embedding_vocab_file = self._get_cosine_matrix(
            embedding, file, vocab_embedding)

        if len(embedding_vocab_file) != len(self._files_vocab[file]):
            return {'Accuracy': np.nan, 'OPP': np.nan}, 0
        
        accuracy = 0
        opp = 0
        for outlier in np.arange(self._cluster_size,
                                 len(self._files_vocab[file])):
            compactness_score = self.calculate_compactness_score(outlier,
                                                                 similarity_matrix,
                                                                 self._cluster_size)
            op, od = self.calculate_op_od(compactness_score, self._cluster_size)
            accuracy += od
            opp += op
        
        return {'Accuracy': accuracy/self._outliers_size,
                'OPP': opp/self._outliers_size}, self._outliers_size

    @staticmethod
    def calculate_op_od(compactness_score: np.ndarray, cluster_size: int) \
            -> tp.Tuple[float, float]:
        """Calculates OP and OD metrics given a compactness score

        :param compactness_score: compactness score of each word
        :type compactness_score: `np.ndarray`
        :param cluster_size: size of the cluster user to detect the outlier
        :type cluster_size: `int`
        :return: A OP and OD metrics
        :rtype: `tp.Tuple[float, float]`
        """
        word_idx = list(range(cluster_size + 1))
        order_idx = [i for _, i in sorted(zip(compactness_score, word_idx),
                                          reverse=True)]
        op = order_idx.index(cluster_size)
        od = op == cluster_size
        return op, od

    @staticmethod
    def calculate_compactness_score(outlier: int,
                                    similarity_matrix: np.ndarray,
                                    cluster_size: int) -> np.ndarray:
        """Calculates pseudo-inverted compactness score

        :param outlier: compactness score of each word
        :type outlier: `int`
        :param similarity_matrix: vocabulary cosine similarity matrix
        :type similarity_matrix: `np.ndarray`
        :param cluster_size: size of the cluster user to detect the outlier
        :type cluster_size: `int`
        :return: a pseudo-inverted compactness score
        :rtype: `np.ndarray`
        """
        len_w = cluster_size + 1
        const_k = 2*(len_w - 1)

        word_idx = list(range(cluster_size))
        word_idx.append(outlier)
        word_idx = np.array(word_idx)
        reduced_matrix = similarity_matrix[word_idx[:, None], word_idx]        

        return (reduced_matrix.sum(axis=0) - 1)/const_k
