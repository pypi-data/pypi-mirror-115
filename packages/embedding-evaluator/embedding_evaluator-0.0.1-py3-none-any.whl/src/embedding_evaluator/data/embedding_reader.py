import typing as tp

from gensim.models import KeyedVectors
from gensim.models.fasttext import FastTextKeyedVectors

from .validate_files import validate_files_path, validate_embedding_models, validate_dict_paths

Model_class = tp.Union[FastTextKeyedVectors]


def read_from_file(file_path: str) -> Model_class:
    """Read a valid file path

    :param file_path: Path for the model
    :type file_path: `str`
    :return: Embedding model
    :rtype: `tp.Union[FastTextKeyedVectors]`
    """
    validate_files_path(file_path)
    model = load_model(file_path)
    validate_embedding_models(model)
    return model


def read_from_files(path_dict: tp.Dict[str, str]) -> tp.Dict[str, Model_class]:
    """Read a valid dictionary of paths

    :param path_dict: A dictionary with the alias and the path of models
    :type path_dict: `tp.Dict[str, str]`
    :return: dictionary with the alias and the loaded models
    :rtype: `tp.Dict[str, Model_class]`

    :raise ValueError: if is a empty dict
    """
    validate_dict_paths(path_dict)
    models_dict = load_models_dict(path_dict)
    return models_dict


def load_model(file_path: str) -> Model_class:
    """Load a valid model

    :param file_path: Path for the model
    :type file_path: `str`
    :return: Valid embedding model
    :rtype: `tp.Union[FastTextKeyedVectors]`

    :raise Exception: if the model type is not accepted
    """
    try:
        model = KeyedVectors.load(file_path)
    except:
        raise Exception('Model type not accepted')
    return model


def load_models_dict(path_dict: tp.Dict[str, str]) -> tp.Dict[str, Model_class]:
    """Load valid models from a dict

    :param path_dict: A dictionary with the alias and the path of models
    :type path_dict: `tp.Dict[str, str]`
    :return: dictionary with the alias and the loaded models
    :rtype: `tp.Dict[str, tp.Union[FastTextKeyedVectors]]`

    :raise AssertionError: if the path is not a string
    :raise Exception: if the path does not exist
    :raise Exception: if the model type is not accepted
    """
    models_dict = {}
    try:
        for name, path in path_dict.items():
            model = read_from_file(path)
            models_dict[name] = model
        return models_dict
    except AssertionError as error:
        raise error
    except Exception as exp:
        if str(exp) == 'File path does not exist':
            raise Exception(f'File path {path} does not exist')
        elif str(exp) == 'Model type not accepted':
            raise Exception(f'Model {name} type not accepted')
