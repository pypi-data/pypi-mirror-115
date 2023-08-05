import os
import typing as tp


def validate_files_path(file_path: tp.Any) -> None:
    """ Validate if the path is a string and exist

    :param file_path: the path to be validate
    :type file_path: `tp.Any`

    :raise AssertionError: if the path is not a string
    :raise Exception: if the path does not exist
    """
    assert type(file_path) == str
    if not os.path.exists(file_path):
        raise Exception(f'File path {file_path} does not exist')


def validate_analogy_format(line: tp.List[str], path: str) -> None:
    """Validate if the line is on pre defined format

    Format for analogy: 4 columns.

    :param line: list representing a line of the file
    :type line: `tp.List[str]`
    :param path: path of the file
    :type path: `str`
    """
    if len(line) not in (4, 0):
        raise Exception(f'Wrong format in file {path}')


def validate_outlier_format(line: tp.List[str], path: str) -> None:
    """Validate if the line is on pre defined format

        Format for outlier detection: 1 column.

        :param line: list representing a line of the file
        :type line: `tp.List[str]`
        :param path: path of the file
        :type path: `str`
        """
    if len(line) not in (1, 0):
        raise Exception(f'Wrong format in file {path}')
