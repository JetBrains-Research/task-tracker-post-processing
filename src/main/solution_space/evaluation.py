import os
import logging
import re
from typing import List, Tuple, Optional

from src.main.util.log_util import log_and_raise_error
from src.main.util.consts import INT_EXPERIENCE, LOGGER_NAME
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.language_util import get_extension_by_language
from src.main.solution_space.path_finder_test_system import TestInput, TestSystem
from src.main.solution_space.consts import EVALUATION_TYPE, EVALUATION_FRAGMENTS_PATH
from src.main.util.file_util import get_all_file_system_items, extension_file_condition, get_content_from_file

log = logging.getLogger(LOGGER_NAME)


class Evaluation:
    def __init__(self, graph: SolutionGraph,  path_to_fragments: str = EVALUATION_FRAGMENTS_PATH):
        self._graph = graph
        self._language = graph.language
        self._task = graph.task
        self._path_to_fragments = path_to_fragments

    def evaluate(self, evaluation_type: EVALUATION_TYPE) -> None:
        test_system = TestSystem(test_inputs=self.get_test_inputs(evaluation_type), graph=self._graph,
                                 to_visualize_graph=False)

    def get_fragments_and_rates(self, evaluation_type: EVALUATION_TYPE) -> Tuple[List[str], List[float]]:
        task_path = os.path.join(self._path_to_fragments, str(self._language.value), str(evaluation_type.value),
                                 str(self._task.value))
        if os.path.exists(task_path):
            extension = get_extension_by_language(self._language)
            fragment_files = get_all_file_system_items(task_path, extension_file_condition(extension))
            fragments_with_rates = list(map(self.__get_fragment_with_rate_from_file, fragment_files))
            return map(list, zip(*fragments_with_rates))
        else:
            log_and_raise_error(f'No fragments found in path {task_path}', log, NotImplementedError)

    def get_test_inputs(self, evaluation_type: EVALUATION_TYPE) -> List[TestInput]:
        if evaluation_type == EVALUATION_TYPE.HINTS:
            # In this type we want to test hints generation, so we decided to take average age and experience
            fragments, rates = self.get_fragments_and_rates(evaluation_type)
            print(rates)
            # Todo: find out real average age and experience
            return TestSystem.generate_all_test_inputs([16], [INT_EXPERIENCE.FROM_ONE_TO_TWO_YEARS], fragments, rates)
        elif evaluation_type == EVALUATION_TYPE.PROFILE:
            # In this type we want to test profile influence on hint generation, so we decided to take few fragments
            # with different age and experience
            fragments, rates = self.get_fragments_and_rates(evaluation_type)
            ages = [10, 40]
            experiences = [INT_EXPERIENCE.LESS_THAN_HALF_YEAR, INT_EXPERIENCE.MORE_THAN_SIX]
            return TestSystem.generate_all_test_inputs(ages, experiences, fragments, rates)
        else:
            log_and_raise_error(f'No test inputs found for evaluation type {evaluation_type}', log, NotImplementedError)

    # Get rate from first line in file if it's possible
    @staticmethod
    def __get_fragment_with_rate_from_file(file: str) -> Tuple[str, Optional[float]]:
        content = f'{get_content_from_file(file)}\n'
        try:
            first_line, rest_content = content.split('\n', 1)
        except ValueError:
            return content, None
        m = re.search(r'# rate: (\d*\.\d+|\d+)', first_line)
        # If there is no line with commented rate, we should return full content with None rate
        if m is None:
            return content, None
        else:
            return rest_content, float(m.group(1))


content = '# rate 0\n\n\n'
first_line, rest_content = content.split('\n', 1)
