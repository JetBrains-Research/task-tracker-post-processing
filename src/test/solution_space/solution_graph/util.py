import ast
from typing import Tuple, List

from src.main.util.consts import TEST_RESULT
from src.main.solution_space.data_classes import Code, User
from src.main.solution_space.solution_graph import SolutionGraph, Vertex


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


# Reset graph, vertex and code last ids to avoid different ids in one-by-one test running and running them all at once
def init_default_ids() -> None:
    SolutionGraph._last_id = 0
    Vertex._last_id = 0
    Code._last_id = 0
    User._last_id = 0
