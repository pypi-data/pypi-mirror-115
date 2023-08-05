from typing import Tuple

import networkx as nx
from networkx import DiGraph
from ply import yacc

from .tex_lex import lexer, tokens

precedence = (("left", "LMB"), ("right", "RMB"))


def parse(s: str) -> DiGraph:
    graph = nx.DiGraph()
    identity = 0

    def _find_rightmost(idx: int) -> int:
        for ni in graph.adj[idx].keys():
            if graph.nodes[ni]["relation"][1] == "R":
                return _find_rightmost(ni)
        return idx

    def p_expression(p):
        """expression : exp"""
        p[0] = p[1]

    def p_frac(p):
        """frac : FRAC char char
        | FRAC bound_exp char
        | FRAC char bound_exp
        | FRAC bound_exp bound_exp"""
        nonlocal identity

        graph.add_node(identity, value=p[1])
        graph.add_edge(identity, p[2])
        graph.nodes[p[2]]["relation"] = (identity, "Above")
        graph.add_edge(identity, p[3])
        graph.nodes[p[3]]["relation"] = (identity, "Below")
        p[0] = identity

        identity += 1

    def p_sqrt(p):
        """sqrt : SQRT char
        | SQRT bound_exp"""
        nonlocal identity

        graph.add_node(identity, value=p[1])
        graph.add_edge(identity, p[2])
        graph.nodes[p[2]]["relation"] = (identity, "Inside")
        p[0] = identity

        identity += 1

    def p_sqrt_above(p):
        """sqrt : SQRT mb_exp char
        | SQRT mb_exp bound_exp"""
        nonlocal identity

        graph.add_node(identity, value=p[1])
        graph.add_edge(identity, p[2])
        graph.nodes[p[2]]["relation"] = (identity, "Above")
        graph.add_edge(identity, p[3])
        graph.nodes[p[3]]["relation"] = (identity, "Inside")
        p[0] = identity

        identity += 1

    def p_middle_bound_exp(p):
        """mb_exp : LMB chars RMB"""
        p[0] = p[2]

    def p_chars(p):
        """chars : char
        | char chars"""
        if len(p) > 2:
            graph.add_edge(p[1], p[2])
            graph.nodes[p[2]]["relation"] = (p[1], "R")
        p[0] = p[1]

    def p_bound_exp(p):
        """bound_exp : LB exp RB"""
        p[0] = p[2]

    def p_left_exp_sup_sub(p):
        """pb_exp : left_single_exp SUP single_exp
        | left_single_exp SUB single_exp"""
        rel = "Sup" if p[2] == "^" else "Sub"
        graph.add_edge(p[1], p[3])
        graph.nodes[p[3]]["relation"] = (p[1], rel)
        p[0] = p[1]

    def p_right_exp_sup_sub(p):
        """pb_exp : right_single_exp SUP single_exp
        | right_single_exp SUB single_exp"""
        rel = "Sup" if p[2] == "^" else "Sub"
        right_idx = _find_rightmost(p[1])

        graph.add_edge(right_idx, p[3])
        graph.nodes[p[3]]["relation"] = (right_idx, rel)
        p[0] = p[1]

    def p_two_left_exp_sup_sub(p):
        """pb_exp : left_single_exp SUP single_exp SUB single_exp
        | left_single_exp SUB single_exp SUP single_exp"""
        rel1 = "Sup" if p[2] == "^" else "Sub"
        rel2 = "Sup" if p[4] == "^" else "Sub"
        graph.add_edge(p[1], p[3])
        graph.nodes[p[3]]["relation"] = (p[1], rel1)
        graph.add_edge(p[1], p[5])
        graph.nodes[p[5]]["relation"] = (p[1], rel2)
        p[0] = p[1]

    def p_two_right_exp_sup_sub(p):
        """pb_exp : right_single_exp SUP single_exp SUB single_exp
        | right_single_exp SUB single_exp SUP single_exp"""
        rel1 = "Sup" if p[2] == "^" else "Sub"
        rel2 = "Sup" if p[4] == "^" else "Sub"
        right_idx = _find_rightmost(p[1])

        graph.add_edge(right_idx, p[3])
        graph.nodes[p[3]]["relation"] = (right_idx, rel1)
        graph.add_edge(right_idx, p[5])
        graph.nodes[p[5]]["relation"] = (right_idx, rel2)
        p[0] = p[1]

    def p_exp_right(p):
        """exp : group_exp exp"""
        graph.add_edge(p[1], p[2])
        graph.nodes[p[2]]["relation"] = (p[1], "R")
        p[0] = p[1]

    def p_right_exp_right(p):
        """exp : right_single_exp exp"""
        right_idx = _find_rightmost(p[1])
        graph.add_edge(right_idx, p[2])
        graph.nodes[p[2]]["relation"] = (right_idx, "R")
        p[0] = p[1]

    def p_exp(p):
        """exp : group_exp
        | right_single_exp"""
        p[0] = p[1]

    def p_group_exp(p):
        """group_exp : left_single_exp
        | pb_exp"""
        p[0] = p[1]

    def p_single_exp(p):
        """single_exp : left_single_exp
        | right_single_exp"""
        p[0] = p[1]

    def p_left_single_exp(p):
        """left_single_exp : char
        | frac
        | sqrt"""
        p[0] = p[1]

    def p_right_single_exp(p):
        """right_single_exp : bound_exp"""
        p[0] = p[1]

    def p_single_mb(p):
        """left_single_exp : LMB
        | RMB"""
        nonlocal identity

        graph.add_node(identity, value=p[1])
        p[0] = identity

        identity += 1

    def p_char(p):
        """char : CHAR"""
        nonlocal identity

        graph.add_node(identity, value=p[1])
        p[0] = identity

        identity += 1

    def p_error(p):
        raise RuntimeError(f"Syntax error at {p.value!r}")

    lr_parser = yacc.yacc()
    lr_parser.parse(s, lexer)
    return graph
