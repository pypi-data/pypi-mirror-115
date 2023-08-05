import os
import typing as tp

from gensim.models.fasttext import FastTextKeyedVectors

models_types = [FastTextKeyedVectors]


def validate_files_path(file_path: tp.Any) -> None:
    """ Validate if the path is a string and exist

    :param file_path: the path to be validate
    :type file_path: `tp.Any`

    :raise AssertionError: if the path is not a string
    :raise Exception: if the path does not exist
    """
    assert type(file_path) == str
    if not os.path.exists(file_path):
        raise Exception('File path does not exist')


def validate_dict_paths(path_dict: tp.Any) -> None:
    """Validate the class and the length of the dictionary with the paths

    :param path_dict: the set of paths to be test
    :type path_dict: `tp.Any`

    :raise AssertionError: if the input is not a dict
    :raise ValueError: if is a empty dict
    """
    assert type(path_dict) == dict
    if len(path_dict) == 0:
        raise ValueError


def validate_analogy_files():
    pass


def validate_outlier_files():
    pass


def validate_embedding_models(model: tp.Any) -> None:
    """ Validate if the model is valid

    :param model: a model to be validate
    :type model: `tp.Any`

    :raise AssertionError: if the model is not accepted
    """
    try:
        assert type(model) in models_types
    except AssertionError:
        raise Exception('Model type not accepted')
