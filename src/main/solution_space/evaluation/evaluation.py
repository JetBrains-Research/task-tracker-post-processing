import logging

from src.main.util.consts import LOGGER_NAME
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.path_finder_test_system import TestSystem
from src.main.solution_space.evaluation.pseudo_solutions_sampling import sample_n_correct_test_inputs

log = logging.getLogger(LOGGER_NAME)


class Evaluation:
    def __init__(self, graph: SolutionGraph,  path_to_fragments: str = '/home/elena/workspaces/python/codetracker-data/data/codetracker-dataset/row_data/python_pies_pseudo_solutions'):
        self._graph = graph
        self._language = graph.language
        self._task = graph.task
        self._path_to_fragments = path_to_fragments

    def evaluate(self, test_inputs_number: int) -> None:
        test_inputs = sample_n_correct_test_inputs(self._path_to_fragments, test_inputs_number)
        test_system = TestSystem(test_inputs=test_inputs, graph=self._graph, to_visualize_graph=False)

