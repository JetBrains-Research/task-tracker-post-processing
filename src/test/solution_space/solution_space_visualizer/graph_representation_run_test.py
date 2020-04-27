# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pytest

from src.main.util.consts import TASK
from src.test.util import to_skip, TEST_LEVEL
from src.test.solution_space.util import get_solution_graph
from src.main.solution_space.solution_graph import SolutionGraph
from src.test.solution_space.solution_graph.util import init_default_ids
from src.main.solution_space.solution_space_visualizer import SolutionSpaceVisualizer

CURRENT_TASK = TASK.PIES


def get_graph() -> SolutionGraph:
    init_default_ids()
    return get_solution_graph(CURRENT_TASK, to_plot_graph=False)


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestRunGraphRepresentation:

    def test_run_graph_representation(self) -> None:
        graph = get_graph()
        visualizer = SolutionSpaceVisualizer(graph)
        visualizer.create_graph_representation()