import pandas as pd
import typing as tp
from .summary import Summary


def update_compare_dict(name: str, compare: dict, summary: dict) -> None:
    """Update dictionary with the metrics

    :param name: Embedding name
    :type name: `str`
    :param compare: Dictionary with the DataFrame comparing each model.
    :type compare: `dict`
    :param summary: Dictionary with summary of metric for a embedding model.
    :type summary: `dict`
    :return:
    """
    for key, value in summary.items():
        for column in value.columns:
            name_column = name + column
            compare[key][name_column] = value[column]


class Compare:
    """
    This class compare different models of embedding in each metric used to
    summarise a evaluate an embedding.

    Attributes:
    :summary Summary - Summary object for metrics

    Methods:
    :get_metrics - Return a DataFrame comparing each model on each metric.
    """

    def __init__(self, summary: Summary) -> None:
        """Initializes the class to compare

        :param summary: object to summarize a model evaluation
        :type summary: `Summary`
        """
        self._summary = summary

    def get_metrics(self, embeddings: dict,
                    vocab: tp.Optional[list] = None) -> dict:
        """Generate the dictionary with the comparation of each metric

        In the output dictionary the key is the metric and the value is the
        DataFrame comparing each model.

        :param embeddings: Dictionary with the models pre-loaded.
        :type embeddings: `dict`
        :param vocab: Embedding vocabulary
        :type vocab: `tp.Optional[list]`
        :return: Dictionary with the DataFrame comparing for each metric
        :rtype: `dict`
        """
        compare_dict = self._generate_compare_dict()
        for name, embedding in embeddings.items():
            summary_dict = self._summary.get_metrics(embedding, vocab)
            update_compare_dict(name, compare_dict, summary_dict)
        return compare_dict

    def _generate_compare_dict(self) -> dict:
        """Generate a empty dictionary to register the metrics values

        :return: Dictionary with a empty DataFrame for each metric
        :rtype: `dict`
        """
        compare_dict = {}
        for metric, file_names in self._summary.files_names.items():
            compare_dict[metric] = pd.DataFrame(index=file_names + ['Total'])
        return compare_dict
