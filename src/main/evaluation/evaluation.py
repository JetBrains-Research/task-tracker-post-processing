# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import timeit
import logging
from functools import partial
from typing import Tuple, List, Type, Optional

from src.main.solution_space.hint import HintHandler
from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.consts import LOGGER_NAME, TEST_RESULT, EXTENSION
from src.main.solution_space.path_finder_test_system import TestSystem
from src.main.solution_space.path_finder.path_finder import IPathFinder
from src.main.solution_space.path_finder.path_finver_v_5 import PathFinderV5
from src.main.solution_space.measured_tree.measured_tree import IMeasuredTree
from src.main.solution_space.measured_tree.measured_tree_v_7 import MeasuredTreeV7
from src.main.evaluation.pseudo_solutions_sampling import sample_n_correct_test_inputs
from src.main.solution_space.consts import TEST_INPUT, EVALUATION_PATH, EVALUATION_FRAGMENT_PATH
from src.main.canonicalization.canonicalization import get_canon_tree_from_anon_tree, get_imports, are_asts_equal, \
    get_code_from_tree
from src.main.util.file_util import get_content_from_file, create_file, deserialize_data_from_file, \
    serialize_data_and_write_to_file

log = logging.getLogger(LOGGER_NAME)


class Evaluation:
    # Either pass pseudo_solutions_path and test_inputs number to sample random test_inputs, or they will be restored
    # from previously stored test_inputs. You can also set store_test_inputs flag to store current inputs.
    def __init__(self, graph: SolutionGraph, pseudo_solutions_path: Optional[str] = None,
                 test_inputs_number: Optional[int] = None, store_test_inputs: bool = True,
                 path_finder: Type[IPathFinder] = PathFinderV5, measured_tree: Type[IMeasuredTree] = MeasuredTreeV7):
        self._graph = graph
        self._language = graph.language
        self._task = graph.task
        self._hint_handler = HintHandler(graph)
        self._path_finder = path_finder(graph, measured_tree)
        test_inputs_file = os.path.join(EVALUATION_PATH,
                                        f'{self._task.value}_test_inputs_indices{EXTENSION.PICKLE.value}')
        if pseudo_solutions_path and test_inputs_number:
            self._test_inputs = sample_n_correct_test_inputs(pseudo_solutions_path, test_inputs_number)
        else:
            try:
                self._test_inputs = deserialize_data_from_file(test_inputs_file)
            except OSError:
                log_and_raise_error(f'OSError during restoring test_inputs from path {test_inputs_file}.', log, OSError)

        print(self._test_inputs)
        if store_test_inputs:
            serialize_data_and_write_to_file(test_inputs_file, self._test_inputs)

    # Creates an .html file with results table with test_inputs_number random test_inputs and hints for them
    def evaluate(self) -> None:
        TestSystem(test_inputs=self._test_inputs, graph=self._graph, to_visualize_graph=False)

    # Evaluates time of getting hint on test_input_number random test_inputs and return results as list of
    # time, nodes_number and test_input index for each of test_inputs
    def evaluate_time(self, test_inputs_number: int, repeat: int = 3) -> List[Tuple[float, int, str]]:
        results = []
        all_time = 0
        for i, t_i in enumerate(self._test_inputs):
            log.info(f'Run {i} test_input')
            anon_tree, canon_tree = TestSystem.create_user_trees(self._hint_handler, t_i)

            def to_time():
                self._path_finder.find_next_anon_tree(anon_tree, canon_tree)

            time = min(timeit.Timer(partial(to_time)).repeat(3, repeat)) / repeat
            log.info(f'time: {time}')
            results.append((time, anon_tree.nodes_number, t_i[TEST_INPUT.INDEX]))
            all_time += time
        log.info(results)
        log.info(all_time)

        return results

    # Check if following our tips will lead to the full solution, for each test_input returns does lead to
    # the full solution and number of steps before stopping getting hints
    def does_lead_to_full_solution(self, test_inputs_number: int) -> List[Tuple[bool, int]]:
        results = []
        for i, t_i in enumerate(self._test_inputs):
            print(f'Run {i}/{len(self._test_inputs)} test input, len: {len(t_i[TEST_INPUT.SOURCE_CODE])}')
            log.info(f'Run {i}/{len(self._test_inputs)} test input')
            anon_tree, canon_tree = TestSystem.create_user_trees(self._hint_handler, t_i)
            prev_anon_trees = [anon_tree.tree]
            steps_n = 0
            get_same_tree = False
            # Keep getting hints until reaching the full solution or getting the same tree again (it means that
            # there is a loop, so we cannot lead to the full solution)
            while anon_tree.rate != TEST_RESULT.FULL_SOLUTION.value and not get_same_tree:
                log.info(f'step: {steps_n}, anon tree:\n {get_code_from_tree(anon_tree.tree)}')
                anon_tree = self._path_finder.find_next_anon_tree(anon_tree, canon_tree,
                                                                  f'test_result_{i}_step_{steps_n}')
                canon_tree = get_canon_tree_from_anon_tree(anon_tree.tree, get_imports(anon_tree.tree))
                steps_n += 1
                # Check for getting the same tree again
                for i, prev_anon_tree in enumerate(prev_anon_trees):
                    print(f'{i} ', end='')
                    if are_asts_equal(anon_tree.tree, prev_anon_tree):
                        log.info(f'Get the same tree, step {steps_n}')
                        get_same_tree = True
                        break
                prev_anon_trees.append(anon_tree.tree)
            results += [(not get_same_tree, steps_n)]
        print(f'results: {results}')
        log.info(f'results: {results}')

        return results

    # Generates N = len(name_suffices) files for evaluation, each of them contains
    # evaluation_fragment (taken from given path), repeated N = len(self._test_inputs) times.
    def generate_file_for_evaluation(self, name_suffices: List[str] = None,
                                     evaluation_fragment_file: str = EVALUATION_FRAGMENT_PATH) -> None:
        # Todo: not sure is it right to write our names here
        if name_suffices is None:
            name_suffices = ['nastya', 'alyona']
        fragment = get_content_from_file(evaluation_fragment_file, to_strip_nl=False)
        fragments = [f'{t_i[TEST_INPUT.INDEX]}.\n{fragment}' for t_i in self._test_inputs]
        evaluation_content = ''.join(fragments)
        for name_suffix in name_suffices:
            evaluation_file = os.path.join(EVALUATION_PATH,
                                           f'{self._task.value}_evaluation_file_{name_suffix}{EXTENSION.TXT.value}')
            create_file(evaluation_content, evaluation_file)
