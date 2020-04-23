# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from enum import Enum
from typing import Callable, Tuple

import pytest

from src.test.util import to_skip, TEST_LEVEL
from src.main.util.consts import TASK, EXTENSION
from src.main.util.file_util import get_content_from_file
from src.test.solution_space.util import get_solution_graph
from src.main.solution_space.solution_graph import SolutionGraph
from src.test.solution_space.solution_graph.util import init_default_ids
from src.main.solution_space.consts import SOLUTION_SPACE_TEST_FOLDER
from src.main.solution_space.solution_space_visualizer import SolutionSpaceVisualizer
from src.test.canonicalization.diffs.diff_handler.util import __get_code_by_source


CURRENT_TASK = TASK.PIES


class GRAPH_TYPE(Enum):
    EMPTY_GRAPH = 'empty_graph'
    SIMPLE = 'simple_graph'
    LOOP = 'graph_with_loop'
    pass


CODE_FOR_LOOP_1 = 'a = int(input())\nb = int(input())\nn = int(input())'
CODE_FOR_LOOP_2 = 'a=int(input())\nb=int(input())\nn=int(input())\nr=a*n\nc=b*n\nwhile c>=100:\n    r+=1\n    c-=100'


def get_empty_graph() -> SolutionGraph:
    init_default_ids()
    return SolutionGraph(CURRENT_TASK)


def get_simple_graph() -> SolutionGraph:
    init_default_ids()
    return get_solution_graph(CURRENT_TASK, to_plot_graph=False)


def get_graph_with_loop() -> SolutionGraph:
    simple_graph = get_simple_graph()
    code_for_loop_1 = __get_code_by_source(CODE_FOR_LOOP_1)
    code_for_loop_2 = __get_code_by_source(CODE_FOR_LOOP_2)
    vertex_for_loop_1 = simple_graph.find_vertex(code_for_loop_1)
    vertex_for_loop_2 = simple_graph.find_vertex(code_for_loop_2)
    vertex_for_loop_2.add_parent(vertex_for_loop_1)
    vertex_for_loop_1.add_parent(vertex_for_loop_2)
    return simple_graph


def get_expected_graph_representation(graph_type: GRAPH_TYPE) -> str:
    file_path = os.path.join(SOLUTION_SPACE_TEST_FOLDER, 'solution_space_visualizer',
                             graph_type.value + EXTENSION.DOT.value)
    return get_content_from_file(file_path)


def get_graph_representation(graph: SolutionGraph) -> str:
    visualizer = SolutionSpaceVisualizer(graph)
    return visualizer._SolutionSpaceVisualizer__get_graph_representation()


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestGraphRepresentation:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (get_empty_graph(), get_expected_graph_representation(GRAPH_TYPE.EMPTY_GRAPH)),
                        (get_simple_graph(), get_expected_graph_representation(GRAPH_TYPE.SIMPLE)),
                        (get_graph_with_loop(), get_expected_graph_representation(GRAPH_TYPE.LOOP))
                    ],
                    ids=[
                        'Empty graph has only the end vertex',
                        'Simple graph without loops from src.test.solution_space.util',
                        'Simple graph from src.test.solution_space.util, but with with loop'
                    ]
                    )
    def param_graph_representation_test(request) -> Tuple[SolutionGraph, str]:
        return request.param

    def test_graph_representation(self, param_graph_representation_test: Callable) -> None:
        graph, expected_representation = param_graph_representation_test
        assert get_graph_representation(graph) == expected_representation


