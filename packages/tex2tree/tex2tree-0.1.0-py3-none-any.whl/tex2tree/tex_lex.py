import os

from ply import lex

dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dictionary.txt")
chars = []
with open(dict_path, "r") as f:
    for line in f.readlines():
        chars.append(line.strip())

tokens = ("CHAR", "SUB", "SUP", "LB", "RB", "LMB", "RMB", "FRAC", "SQRT")

t_CHAR = "|".join(chars)
t_SUB = r"_"
t_SUP = r"\^"
t_LB = r"{"
t_RB = r"}"
t_LMB = r"\["
t_RMB = r"\]"
t_FRAC = r"\\frac"
t_SQRT = r"\\sqrt"

t_ignore = "\t\r\n "


def t_bigg(t):
    r"\\Bigg"
    pass


def t_big(t):
    r"\\Big"
    pass


def t_mbox(t):
    r"\\mbox"
    pass


def t_mathrm(t):
    r"\\mathrm"
    pass


def t_left(t):
    r"\\left(?!arrow)"
    pass


def t_right(t):
    r"\\right(?!arrow)"
    pass


def t_error(t):
    raise RuntimeError(f"Illegal character {t.value[0]!r}")


lexer = lex.lex()
