import typing as tp


def get_vocab(model: tp.Any) -> tp.List[str]:
    """Get model vocabulary

    :param model: Embedding model
    :type model: `tp.Any`
    :return: List with the vocabulary
    :rtype: `tp.List[str]`
    """
    return [word for word in model.vocab]


def get_vocab_models(models: tp.Dict[str, tp.Any]) -> tp.List[str]:
    """Get vocabulary of the models

    :param models: Dictionary with the embedding model
    :type models: `tp.Dict[str, tp.Any]`
    :return: List with the vocabulary
    :rtype: `tp.List[str]`
    """
    models_vocabs = [get_vocab(model) for model in models.values()]
    vocab = list(set(models_vocabs[0]).intersection(*models_vocabs[1:]))
    return vocab
