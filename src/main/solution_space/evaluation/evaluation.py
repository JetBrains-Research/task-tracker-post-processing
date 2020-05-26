import logging
import re
from enum import Enum

from src.main.util.consts import LOGGER_NAME, UTF_ENCODING
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.path_finder_test_system import TestSystem
from src.main.solution_space.evaluation.pseudo_solutions_sampling import sample_n_correct_test_inputs
from src.main.util.file_util import create_file, get_content_from_file

log = logging.getLogger(LOGGER_NAME)


class Evaluation:
    def __init__(self, graph: SolutionGraph,
                 path_to_fragments: str = '/home/elena/workspaces/python/codetracker-data/data/codetracker-dataset/row_data/python_brackets_pseudo_solutions'):
        self._graph = graph
        self._language = graph.language
        self._task = graph.task
        self._path_to_fragments = path_to_fragments

    def evaluate(self, test_inputs_number: int) -> None:
        test_inputs = sample_n_correct_test_inputs(self._path_to_fragments, test_inputs_number)
        test_system = TestSystem(test_inputs=test_inputs, graph=self._graph, to_visualize_graph=False)


file = '/home/elena/workspaces/python/codetracker-data/src/resources/evaluation/brackets_evaluation_file_alyona.txt'
content = ''
n = 100
eval_fragment = 'не решение:\n' \
                '\t\tподсказка маленькая\n' \
                '\t\tподсказка большая\n\n\n' \
                'решение:\n' \
                '\t\tструктура подсказки похожа\n' \
                '\t\tструктура подсказки непохожа\n\n' \
                '\t\tподсказка приблизила к решению\n' \
                '\t\tподсказка выдала то же дерево\n' \
                '\t\tподсказка отдалила от решения\n' \
                '\t\tнепонятно, отдалила или приблизила\n\n' \
                '\t\tшаг подсказки ок\n' \
                '\t\tшаг подсказки большой\n' \
                '\t\tшаг подсказки маленький\n\n' \
                '\t\tподсказка хорошая\n' \
                '\t\tподсказка нормальная\n' \
                '\t\tподсказка плохая\n\n' \
                '\t\tдиффы корректно\n' \
                '\t\tдиффы некорректно\n\n\n\n\n'

for i in range (n):
    content += f'{i}.\n{eval_fragment}'

create_file(content, file)

