# Copyright (c) by anonymous author(s)
import os
from typing import Callable

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.consts import TASK, TEST_DATA_PATH
from src.test.solution_space.util import get_solution_graph
from src.main.util.file_util import get_all_file_system_items
from src.main.util.helper_classes.id_counter import IdCounter
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer


CURRENT_TASK = TASK.PIES

TEST_SERIALIZED_GRAPH = os.path.join(TEST_DATA_PATH, 'solution_space/solution_space_serializer/graph.pickle')


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
                        get_solution_graph(CURRENT_TASK)
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

    def test_id_counter_serialization(self) -> None:
        IdCounter.reset_all()
        deserialized_graph = SolutionSpaceSerializer.deserialize(TEST_SERIALIZED_GRAPH)
        for vertex in deserialized_graph.get_traversal(to_remove_start=False, to_remove_end=False):
            assert vertex == Vertex.get_item_by_id(vertex.id)
