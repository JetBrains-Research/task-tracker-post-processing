import ast
from typing import Tuple, List

from src.main.solution_space.data_classes import Code
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.util.consts import TEST_RESULT


def create_code_from_source(source: str, rate: int = TEST_RESULT.CORRECT_CODE.value) -> Code:
    return Code(ast.parse(source), rate)


def __get_two_sources_and_rates() -> Tuple[List[str], List[int]]:
    source_0 = 'print(\'Hi\')'
    source_1 = 'x = True\nif(x):\n    x = False\nprint(x)'
    sources = [source_0, source_1]
    rates = [TEST_RESULT.CORRECT_CODE.value] * len(sources)
    return sources, rates


def get_two_vertices(sg: SolutionGraph) -> List[Vertex]:
    sources, rates = __get_two_sources_and_rates()
    return [Vertex(sg, code=create_code_from_source(s, rates[i])) for i, s in enumerate(sources)]
