import typing as tp
import pandas as pd

from embedding_evaluator.data import data_reader, embedding_reader, \
    validate_input
from embedding_evaluator.logic import summary, compare, vocab


class EmbeddingMetrics:
    """
    This class has the objective of evaluate embedding models based on a list
    of files of different metrics to evaluate the embedding.

    :Attributes:
    :input_metrics dict - Dictionary with path to the metrics files.:
    :input_embedding dict - Dictionary with path to the models.:
    :sep str - Separator of the files:

    :Methods:
    :summary metrics - Summary a model in the dictionary of models:
    :compare_metrics - Compare a list of models:
    """

    def __init__(self, input_metrics: tp.Dict[str, tp.List[str]],
                 input_embedding: tp.Dict[str, str], sep: str = ' '):
        """Initialize EmbeddingMetrics

        :param input_metrics: Dictionary with path to the metrics files.
        :type input_metrics: `tp.Dict[str, tp.List[str]]`
        :param input_embedding: Dictionary with path to the models.
        :type input_embedding: `tp.Dict[str, str]`
        :param sep: Separator of the files
        :type sep: `str`
        """
        validate_input.validate_input(input_metrics, input_embedding)
        self._read_files(input_metrics, sep)
        self._read_embedding(input_embedding)
        self._summary = summary.Summary(self.dict_files)
        self._compare = compare.Compare(self._summary)

    def _read_embedding(self, input_embedding: tp.Dict[str, str]) -> None:
        """Read all embedding models

        :param input_embedding: Dictionary with path to the models.
        :type input_embedding: `dict`
        """
        self.dict_models = {}
        for key, value in input_embedding.items():
            self.dict_models[key] = embedding_reader.read_from_file(value, key)

    def _read_files(self, input_metrics: tp.Dict[str, tp.List[str]],
                    sep: str = ' ') -> None:
        """Read all files

        :param input_metrics: Dictionary with path to the metrics files.
        :type input_metrics: `dict`
        :param sep: Separator of the files
        :type sep: `str`
        """
        self.dict_files = {}
        for key, value in input_metrics.items():
            self.dict_files[key] = {}
            for file in value:
                self.dict_files[key][file] = data_reader.load_files(file, key,
                                                                    sep)

    def summary_metrics(self, model_name: str,
                        use_oov: bool = True) -> tp.Dict[str, pd.DataFrame]:
        """Summary a model in the dictionary of models

        :param model_name: Name of model to be evaluated.
        :type model_name: `str`
        :param use_oov: Flag defining the use of oov words. Defaults to True.
        :type use_oov: `bool`
        :return: Dictionary with the summary of each metric
        :rtype: `tp.Dict[str, pd.DataFrame]`
        """
        if model_name not in self.dict_models.keys():
            raise Exception(f'The {model_name} does not exist')
        model = self.dict_models[model_name]
        emb_vocab = vocab.get_vocab(model) if not use_oov else None
        model_summary = self._summary.get_metrics(model, emb_vocab)
        return model_summary

    def compare_metrics(self, model_names: tp.List[str],
                        use_oov: bool = True) -> tp.Dict[str, pd.DataFrame]:
        """Compare a list of models

        :param model_names: List with the name of models to be evaluated.
        :type model_names: `tp.List[str]`
        :param use_oov: Flag defining the use of oov words. Defaults to True.
        :type use_oov: `bool`
        :return: Dictionary containing Dataframes with the comparison for each of the metrics.
        :rtype: `tp.Dict[str, pd.DataFrame]`
        """
        models = {}
        for model_name in model_names:
            if model_name not in self.dict_models.keys():
                raise Exception(f'The {model_name} does not exist')
            models[model_name] = self.dict_models[model_name]
        emb_vocab = vocab.get_vocab_models(models) if not use_oov else None
        models_compare = self._compare.get_metrics(models, emb_vocab)
        return models_compare
