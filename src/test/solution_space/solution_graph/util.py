# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
from typing import Tuple, List

from src.main.canonicalization.canonicalization import get_trees, get_code_from_tree
from src.main.canonicalization.consts import TREE_TYPE
from src.main.util.consts import TEST_RESULT
from src.main.solution_space.data_classes import Code, User
from src.main.solution_space.solution_graph import SolutionGraph, Vertex


def create_code_from_source(source: str, rate: float = TEST_RESULT.CORRECT_CODE.value) -> Code:
    canon_tree, = get_trees(source, {TREE_TYPE.CANON})
    print(f'source code is:\n{source}\n\ncode from tree is:\n{get_code_from_tree(canon_tree)}\n\n\n')
    return Code(canon_tree, rate)


def __get_two_sources_and_rates() -> Tuple[List[str], List[int]]:
    source_0 = 'print(\'Hi\')'
    source_1 = 'x = True\nif(x):\n    x = False\nprint(x)'
    sources = [source_0, source_1]
    rates = [TEST_RESULT.CORRECT_CODE.value] * len(sources)
    return sources, rates


def get_two_vertices(sg: SolutionGraph) -> List[Vertex]:
    sources, rates = __get_two_sources_and_rates()
    return [Vertex(sg, code=create_code_from_source(s, rates[i])) for i, s in enumerate(sources)]


# Reset graph, vertex and code last ids to avoid different ids in one-by-one test running and running them all at once
def init_default_ids() -> None:
    SolutionGraph._last_id = 0
    Vertex._last_id = 0
    Code._last_id = 0
    User._last_id = 0
