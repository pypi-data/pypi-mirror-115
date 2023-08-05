import typing as tp

from gensim.models import KeyedVectors

from .validate_files import validate_files_path


def read_from_file(file_path: str,
                   model_name: str = 'unnamed_model') -> tp.Any:
    """Read a valid file path

    :param file_path: Path for the model
    :type file_path: `str`
    :param model_name: Name for the model
    :type model_name: `str`
    :return: Embedding model
    :rtype: `tp.Any`
    """
    validate_files_path(file_path)
    model = load_model(file_path, model_name)
    return model


def load_model(file_path: str, model_name: str) -> tp.Any:
    """Load a valid model

    :param file_path: Path for the model
    :type file_path: `str`
    :param model_name: Name for the model
    :type model_name: `str`
    :return: Valid embedding model
    :rtype: `tp.Union[FastTextKeyedVectors]`

    :raise Exception: if the model type is not accepted
    """
    try:
        model = KeyedVectors.load(file_path)
    except:
        raise Exception(f'Failed to read model {model_name}')
    return model
