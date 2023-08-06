import re


def capletter(s, n):
    """
    Capitalize _n_th letter of string
    """
    aux_list = list(s)
    try:
        aux_list[n] = aux_list[n].upper()
        return "".join(aux_list)
    except IndexError:
        return s


def find_between_quotations(s, q='"'):
    """
    Find substrings between quotations.

    :param s: Input string.
    :param q: Quotation mark type. Default: "
    :return: Substrings found between quotation marks _q_
    """
    try:
        if q == '"':
            return re.findall('"([^"]*)"', str(s))[0]
        elif q == "'":
            return re.findall("'([^']*)'", str(s))[0]
    except IndexError:
        return print('No match')


def join_set_distance(s, u, n=20):
    """
    :param s: String 1
    :param u: String 2
    :param n: Length from the beginning of String 1 to the start of String 2
    :return: Joint strings _s_ and _u_, separated by the necessary whitespace so
             the length from the first character of String 1 to the first of
             String 2 equals _n_.
    """
    if not isinstance(s, type(str)):
        s = str(s)
    m = max(n - len(s.replace("\n", "")), 1)
    return s + ' ' * m + u.rstrip()


def tuple_to_equal(a):
    """
    :param a: Tuple.
    :return: String of the form "tuple[0] = tuple[1]"
    """
    chars = r"()"
    for c in chars:
        if c in a:
            a = a.replace(c, "")
    return a.replace(", ", " = ")
