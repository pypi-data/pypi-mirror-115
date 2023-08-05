import warnings
import typing as tp
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from itertools import chain

representations = tp.Tuple[tp.Optional[np.ndarray], list]


class CalculateMetrics:
    """
    This class implements the embedding representation for the vocabulary and
    similarity matrix between the words in the vocabulary.

    The vocabulary can be extracted from a file or created by the intersection
    of the words on the input file and the embedding vocabulary.

    Attributes:
    :files_vocab (tp.Dict[str, list]) - a dictionary with vocabulary
    """

    def __init__(self, files_vocab: tp.Dict[str, list]):
        """Initializes the class setting the file vocabulary

        :param files_vocab: Dictionary with the file vocabulary.
        :type files_vocab: `tp.Dict[str, list]`
        """
        self._create_vocabulary(files_vocab)

    def _create_vocabulary(self, dict_corpus: tp.Dict[str, list]) -> None:
        """Create vocabulary of each file

        :param dict_corpus: Dictionary with the lines of files.
        :type dict_corpus: dict
        """
        files = dict_corpus.keys()
        self._dict_vocab = {}
        for file in files:
            file_corpus = dict_corpus[file]
            if len(file_corpus) == 0:
                raise Exception(f'File {file} has only empty lines')
            words_all_rows = list(chain(*file_corpus))
            self._dict_vocab[file] = sorted(set(words_all_rows),
                                            key=words_all_rows.index)

    def _remove_out_of_vocabulary(self, embedding_vocabulary: list,
                                  file: str) -> list:
        """Remove words out of embedding vocabulary

        :param embedding_vocabulary: The vocabulary used to build the embedding
        :type embedding_vocabulary: list
        :param file: Name of the file
        :type file: `str`
        :return: A list of words that are in the embedding vocab and in the file
        :rtype: `list`
        """
        file_vocabulary = self._dict_vocab[file]
        return [word for word in file_vocabulary if word in
                embedding_vocabulary]

    def _get_representation(self, embedding: tp.Any, file: str,
                            vocab: tp.Optional[list] = None) -> representations:
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
            vocabulary_list = self._remove_out_of_vocabulary(vocab, file)
        else:
            vocabulary_list = self._dict_vocab[file]
        if len(vocabulary_list) == 0:
            warnings.warn(f'File {file} has no embedding representation')
            return None, vocabulary_list
        return embedding[vocabulary_list], vocabulary_list

    def _get_cosine_matrix(self, embedding: tp.Any, file: str,
                           vocab: tp.Optional[list] = None) -> representations:
        """Get the cosine similarity of the words

        :param embedding: Embedding model used in the analysis.
        :type embedding: `tp.Any`
        :param file: Name of the file to be analysed.
        :type file: `str`
        :param vocab: Embedding vocabulary to remove oov
        :type vocab: `tp.Optional[list]`
        :return: Array of the similarities and the vocabulary used
        :rtype: `tp.Tuple[tp.Optional[np.ndarray], list]`
        """
        representation, vocab_file = self._get_representation(embedding, file,
                                                              vocab)
        if isinstance(representation, type(None)):
            return None, vocab_file
        else:
            return cosine_similarity(representation), vocab_file
