from gensim.models import FastText, Word2Vec
from gensim.test.utils import get_tmpfile


def mock_fasttext():
    model = FastText()
    fname = get_tmpfile('fasttext.kv')
    model.wv.save(fname)
    return fname


def mock_word2vec():
    model = Word2Vec()
    fname = get_tmpfile('word2vec.kv')
    model.wv.save(fname)
    return fname