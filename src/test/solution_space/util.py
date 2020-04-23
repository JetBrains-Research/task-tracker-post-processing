# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from typing import List, Tuple

from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.data_classes import CodeInfo, User
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.consts import TEST_DATA_PATH, TASK, FILE_SYSTEM_ITEM,LOGGER_NAME
from src.test.canonicalization.diffs.diff_handler.util import __get_code_by_source, __plot_graph
from src.main.util.file_util import get_all_file_system_items, match_condition, get_content_from_file

log = logging.getLogger(LOGGER_NAME)

BASE_DATA_PATH = os.path.join(TEST_DATA_PATH, 'solution_space', 'graphs')


def get_user_solutions(task: TASK) -> List[str]:
    root = os.path.join(BASE_DATA_PATH, task.value, 'user_solutions')
    solutions = get_all_file_system_items(root, match_condition(r'source_\d+.py'))
    # We have to know the order
    solutions.sort()
    return [get_content_from_file(f) for f in solutions]


def __get_chains(task: TASK) -> List[Tuple[List[str], str]]:
    root = os.path.join(BASE_DATA_PATH, task.value)
    chains = get_all_file_system_items(root, match_condition(r'chain_\d+'), item_type=FILE_SYSTEM_ITEM.SUBDIR)
    # We have to know ids for vertexes
    chains.sort()
    res_chains = []
    for chain in chains:
        sources_paths = get_all_file_system_items(chain, match_condition(r'source_\d+.py'))
        goals = get_all_file_system_items(chain, match_condition(r'goal.py'))
        if len(goals) != 1:
            log_and_raise_error(f'The chain {chain} contains more than 1 goal', log)
        sources_paths.sort()
        res_chains.append(([get_content_from_file(f) for f in sources_paths], get_content_from_file(goals[0])))
    return res_chains


def get_solution_graph(task: TASK, to_plot_graph: bool = True,
                       test_prefix: str = 'path_finder_test') -> SolutionGraph:
    chains = __get_chains(task)
    sg = SolutionGraph(task)
    code_info = CodeInfo(User())
    for chain in chains:
        sources, goal = chain
        goal_code = __get_code_by_source(goal, is_goal=True)
        codes = [__get_code_by_source(s) for s in sources] + [goal_code]
        chain = [(code, code_info) for code in codes]
        sg.add_code_info_chain(chain)
    if to_plot_graph:
        path = __plot_graph(task, sg, test_prefix)
        log.info(f'Graph path for solution space for task {task.value} is {path}')
    return sg

get_solution_graph(TASK.PIES)