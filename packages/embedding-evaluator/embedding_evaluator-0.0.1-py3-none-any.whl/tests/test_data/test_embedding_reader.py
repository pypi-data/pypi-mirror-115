import pytest
from gensim.models.fasttext import FastTextKeyedVectors
from .mock_model import mock_fasttext, mock_word2vec
from embedding_evaluator.data import embedding_reader


def test_file_path_not_exist():
    mock_path = ' '
    with pytest.raises(Exception, match=r'File path does not exist'):
        embedding_reader.read_from_file(mock_path)


def test_files_path_not_exist():
    file_name = mock_fasttext()
    mock_path = {'model 1': ' ',
                 'model 2': file_name}
    with pytest.raises(Exception, match=r'File path .* does not exist'):
        embedding_reader.read_from_files(mock_path)


def test_type_file_path():
    mock_path = 2
    with pytest.raises(AssertionError):
        embedding_reader.read_from_file(mock_path)


def test_type_files_path():
    mock_path = {'model 1': 2,
                 'model 2': mock_fasttext()}
    with pytest.raises(AssertionError):
        embedding_reader.read_from_files(mock_path)


def test_type_dict_path():
    mock_path = 2
    with pytest.raises(AssertionError):
        embedding_reader.read_from_files(mock_path)


def test_empty_dict():
    mock_path = {}
    with pytest.raises(ValueError):
        embedding_reader.read_from_files(mock_path)


def test_model_type_file():
    mock_file_path = mock_word2vec()
    with pytest.raises(Exception, match=r'Model type not accepted'):
        embedding_reader.read_from_file(mock_file_path)


def test_model_type_files():
    mock_files_path = {'Word2vec': mock_word2vec(),
                       'FastText': mock_fasttext()}
    with pytest.raises(Exception, match=r'Model .* type not accepted'):
        embedding_reader.read_from_files(mock_files_path)


def test_return_model_file():
    mock_path = mock_fasttext()
    model = embedding_reader.read_from_file(mock_path)
    assert type(model) == FastTextKeyedVectors


def test_return_model_files():
    mock_path = {'Model 1': mock_fasttext(),
                 'Model 2': mock_fasttext()}
    model = embedding_reader.read_from_files(mock_path)
    assert type(model) == dict
    assert type(model['Model 1']) == FastTextKeyedVectors
