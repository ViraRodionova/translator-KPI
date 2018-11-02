keywords = {
    'PROGRAM': 401,
    'BEGIN': 402,
    'END': 403,
    'LABEL': 404,
    'GOTO': 405,
    'LINK': 406,
    'IN': 407,
    'OUT': 408
}

empty = [9, 10, 11, 12, 13, 32]
delims = [':', ';', '.', ',']


def is_lt(c):
    return c >= 'A' and c <= 'Z'


def is_dg(c):
    return c >= '0' and c <= '9'


def is_dm(c):
    return c in delims


def is_empty(c):
    return ord(c) in empty


def is_keyword(str):
    return str in keywords.keys()
