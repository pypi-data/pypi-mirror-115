def validate_input(input_metrics: dict, input_embedding: dict) -> None:
    """Validate dictionary with the paths

    :param input_metrics: Dictionary with path to the metrics files.
    :type input_metrics: `dict`
    :param input_embedding: Dictionary with path to the models.
    :type input_embedding: `dict`
    """
    if type(input_metrics) != dict:
        raise ValueError('The input_metrics format is not a dictionary')
    if type(input_embedding) != dict:
        raise ValueError('The input_embedding is not a dictionary')
    if any([type(value) != list for value in input_metrics.values()]):
        raise ValueError('The input_metrics value is not a list')
