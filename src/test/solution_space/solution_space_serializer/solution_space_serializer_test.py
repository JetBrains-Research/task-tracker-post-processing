# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Callable

import pytest

from src.main.util.consts import TASK
from src.test.util import to_skip, TEST_LEVEL
from src.test.solution_space.util import get_solution_graph
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer


CURRENT_TASK = TASK.PIES


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
        graph = param_solution_space_serializer_test
        serialized_path = SolutionSpaceSerializer.serialize(graph)
        deserialized_graph = SolutionSpaceSerializer.deserialize(serialized_path)
        assert str(graph) == str(deserialized_graph)
