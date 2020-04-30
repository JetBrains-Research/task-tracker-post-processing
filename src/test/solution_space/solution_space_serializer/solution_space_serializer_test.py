# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Callable

import pytest

from src.main.util.consts import TASK
from src.test.test_config import to_skip, TEST_LEVEL
from src.test.solution_space.util import get_solution_graph
from src.main.util.file_util import get_all_file_system_items
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer


CURRENT_TASK = TASK.PIES


def are_graph_folder_structures_equal(old_graph_folder: str, new_graph_folder: str):
    old_items = get_all_file_system_items(old_graph_folder)
    old_items.sort()
    new_items = get_all_file_system_items(new_graph_folder)
    new_items.sort()
    return old_items == new_items


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestSolutionSpaceSerializer:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        SolutionGraph(CURRENT_TASK),
                        get_solution_graph(CURRENT_TASK, to_store_dist=False)
                    ],
                    ids=[
                        'Empty SolutionGraph',
                        'Simple graph'
                    ]
                    )
    def param_solution_space_serializer_test(request) -> SolutionGraph:
        return request.param

    def test_graph_representation(self, param_solution_space_serializer_test: Callable) -> None:
        graph: SolutionGraph = param_solution_space_serializer_test
        serialized_path = SolutionSpaceSerializer.serialize(graph)
        deserialized_graph = SolutionSpaceSerializer.deserialize(serialized_path)
        assert are_graph_folder_structures_equal(graph.graph_directory, deserialized_graph.graph_directory)
        assert graph.get_pretty_string() == deserialized_graph.get_pretty_string()
