import numpy as np
import pandas as pd
import typing as tp

from .analogy_metrics import CalculateAnalogy
from .outlier_metrics import OutlierMetrics


def generate_total(summary_df: pd.DataFrame, total_metric: dict,
                   total_size: int) -> pd.DataFrame:
    """ Add the total of a metric based on the result of a list of file

    :param summary_df: DataFrame of the values of metric for each file
    :type summary_df: `pd.DataFrame`
    :param total_metric: Dictionary with the Sum of the metric over the files
    :type total_metric: `dict`
    :param total_size: Sum of the number of words used in each file
    :type total_size: `int`
    :return: DataFrame of summary with additional row for the total
    :rtype: `pd.DataFrame`
    """
    summary_df.append(pd.DataFrame(index=['Total']))
    for key, value in total_metric.items():
        if total_size == 0:
            summary_df.loc['Total', key] = np.nan
        else:
            summary_df.loc['Total', key] = value / total_size
    return summary_df


def update_summary(summary_df: pd.DataFrame, total_metric: dict, file: str,
                   metric_evaluate: dict, size: int) -> \
        tp.Tuple[pd.DataFrame, dict]:
    """Update summary DataFrame with the metric of a file

    :param summary_df: DataFrame of the values of metric for each file
    :type summary_df: `pd.DataFrame`
    :param total_metric: Dictionary with the sum of the metric over the files
    :type total_metric: `dict`
    :param file: File name
    :type file: `str`
    :param metric_evaluate: Dictionary with metric values of a file
    :type metric_evaluate: `dict`
    :param size: Number of words used in the metric calculation
    :type size: `int`
    :return: A tuple with update DataFrame of each metric and updated total
    of the metrics
    :rtype: `tp.Tuple[pd.DataFrame, dict]`
    """
    for key, value in metric_evaluate.items():
        summary_df.loc[file, key] = value
        total_metric[key] = np.nansum([total_metric.get(key, 0),
                                       value * size])
    return summary_df, total_metric


class Summary:
    """
    This class has the objective of summarize a embedding model based on a list
    of files of different metrics to evaluate the embedding.

    Attributes:
    :files dict - Dictionary with the rows of each file:

    Methods:
    :get_metrics - Return a dictionary with the metrics of a model:
    """

    def __init__(self, files: dict):
        """ Initializes the class to summary

        :param files: Dictionary with the row of each metric file
        :type files: `dict`
        """
        self._evaluator = {}
        self.files_names = {}
        self._attributed_analogy(files)
        self._attributed_outlier(files)

    def _attributed_analogy(self, files: dict) -> None:
        """Attribute analogy evaluator if is one of the metric

        :param files: Dictionary with the row of each metric file
        :type files: `dict`
        """
        if 'analogy' in files.keys():
            self._evaluator['analogy'] = CalculateAnalogy(files['analogy'])
            self.files_names['analogy'] = list(files['analogy'].keys())

    def _attributed_outlier(self, files):
        """Attribute analogy evaluator if is one of the metric

        :param files: Dictionary with the row of each metric file
        :type files: `dict`
        """
        if 'outlier' in files.keys():
            self._evaluator['outlier'] = OutlierMetrics(files['outlier'])
            self.files_names['outlier'] = list(files['outlier'].keys())

    def _get_metric_file(self, summary_df: pd.DataFrame, metric: str,
                         embedding: tp.Any, vocab: list) -> pd.DataFrame:
        """Get the metrics of each file

        :param summary_df: DataFrame of the values of metric for each file
        :type summary_df: `pd.DataFrame`
        :param metric: evaluator metric name
        :type metric: `str`
        :param embedding: Embedding model
        :type embedding: `tp.Any`
        :param vocab: List with the vocabulary of the embedding
        :type vocab: `list`
        :return: Updated DataFrame of the values of metric for each file
        :rtype: `pd.DataFrame`
        """
        total_size = 0
        total_row = {}
        for file in self.files_names[metric]:
            evaluate, size = self._evaluator[metric].get_metrics(embedding,
                                                                 file,
                                                                 vocab)
            total_size += size
            summary_df, total_row = update_summary(summary_df, total_row,
                                                   file, evaluate, size)
        summary_df = generate_total(summary_df, total_row, total_size)
        return summary_df

    def get_metrics(self, embedding: tp.Any,
                    vocab: tp.Optional[list] = None) -> dict:
        """Get the dictionary with the summary of a model

        :param embedding: Embedding model
        :type embedding: `tp.Any`
        :param vocab: List with the embedding vocabulary
        :type vocab: `tp.Optional[list]`
        :return: Dictionary with the summary of each metric
        :rtype: `dict`
        """
        output = {}
        for metric in self._evaluator.keys():
            output[metric] = pd.DataFrame(index=self.files_names[metric])
            output[metric] = self._get_metric_file(output[metric], metric,
                                                   embedding, vocab)

        return output
