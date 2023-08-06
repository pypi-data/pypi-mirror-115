def if_none(a, b):
    """
    :param a: Variable 1
    :param b: Variable 2
    :return: a if it's not None, else b
    """
    return b if isinstance(a, type(None)) else a