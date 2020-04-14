# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging

from src.test.test_util import LoggedTest
from src.main.util.file_util import create_file
from src.main.solution_space.data_classes import User
from src.main.solution_space.path_finder import PathFinder
from src.main.canonicalization.diffs.diff_handler import IDiffHandler
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.canonicalization.canonicalization import get_code_from_tree
from src.main.canonicalization.diffs.gumtree_diff_handler import GumTreeDiffHandler
from src.test.solution_space.path_finder.util import get_solution_graph, get_user_solutions
from src.main.util.consts import TASK, LOGGER_NAME, SOLUTION_SPACE_TEST_RESULT_PATH, EXTENSION


log = logging.getLogger(LOGGER_NAME)


SAVE_FOLDER = os.path.join(SOLUTION_SPACE_TEST_RESULT_PATH, 'path_finder')


# Todo: 14/04 calculate user rate
NOT_ZERO_RATES_INDEXES = [4]


def get_res_for_current_test(test_prefix: str, task: TASK, s_g: SolutionGraph,
                             user_dh: IDiffHandler, next_vertex: Vertex) -> str:
    res = ''
    res += f'Task: {task.value}\n'
    res += f'Test prefix for graph_folder: {test_prefix}. Graph id: {s_g.id}\n\n'
    res += f'User original code:\n{get_code_from_tree(user_dh.orig_tree)}\n\n'
    res += f'Next vertex id: {next_vertex.id}\n'
    res += f'Next canon code:\n{get_code_from_tree(next_vertex.code.canon_tree)}\n'
    for i, a_t in enumerate(next_vertex.code.anon_trees):
        res += f'Next anon code {i}:\n{get_code_from_tree(a_t)}\n'
    return res


def run_test(self, task: TASK, test_prefix: str, s_g: SolutionGraph) -> None:
    current_save_folder = os.path.join(SAVE_FOLDER, task.value)
    user_solutions = get_user_solutions(task)
    user = User()
    for i, user_solution in enumerate(user_solutions):
        p_f = PathFinder(s_g)
        user_dh = GumTreeDiffHandler(user_solution)
        user_rate = 0 if i not in NOT_ZERO_RATES_INDEXES else 0.5
        next_vertex = p_f.find_next_vertex(user_dh, user, user_rate=user_rate)
        res = get_res_for_current_test(test_prefix, task, s_g, user_dh, next_vertex)
        current_file_name = os.path.join(current_save_folder, f'user_code_{i}{EXTENSION.TXT.value}')
        create_file(res, current_file_name)
        log.info(res)


class TestPathFinderAlgo(LoggedTest):

    def test_pies_path_finder_algo(self) -> None:
        task = TASK.PIES
        test_prefix = 'path_finder_test'
        s_g = get_solution_graph(task, test_prefix=test_prefix)
        run_test(self, task, test_prefix, s_g)
