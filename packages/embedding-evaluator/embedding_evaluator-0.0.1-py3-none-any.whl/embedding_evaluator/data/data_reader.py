import warnings
import typing as tp

from csv import reader

from .validate_files import validate_files_path, validate_analogy_format, validate_outlier_format


def load_files(path: str, file_type: str, sep: str) -> tp.List[tp.List[str]]:
    """Load a valid csv/txt file

    :param path: Path for the file
    :type path: `str`
    :param file_type: Type of metric associated with the file
    :type file_type: `str`
    :param sep: Separator of the file
    :type sep: `str`
    :return: List with the rows
    :rtype: `tp.List[tp.List[str]]`
    """
    sentences = []
    empty_line = 0
    validate_line = get_validate_function(file_type)
    validate_files_path(path)
    with open(path) as file:
        csv_reader = reader(file, delimiter=sep)
        for row in csv_reader:
            validate_line(row, path)
            if len(row) == 0:
                empty_line += 1
            else:
                sentences.append(row)
    if empty_line > 0:
        warnings.warn(f'File {path} has {empty_line} empty lines')
    return sentences


def get_validate_function(file_type: str) -> callable:
    """ Get a validate function based on a metric type

    :param file_type: Type of metric associated with the file
    :type file_type: `str`
    :return: Function for validation
    """
    validate_dicts = {'analogy': validate_analogy_format,
                      'outlier': validate_outlier_format}
    if file_type not in validate_dicts.keys():
        raise Exception(f'Type {file_type} is not accepted')
    return validate_dicts[file_type]
