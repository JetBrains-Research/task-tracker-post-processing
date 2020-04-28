# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from enum import Enum
from typing import Tuple, List

from src.main.canonicalization.consts import TREE_TYPE
from src.main.canonicalization.canonicalization import get_trees
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.data_classes import CodeInfo, User
from src.main.solution_space.code_1 import Code
from src.main.util.consts import LOGGER_NAME, TEST_DATA_PATH, TASK, TEST_RESULT
from src.main.solution_space.solution_space_visualizer import SolutionSpaceVisualizer
from src.main.util.file_util import get_content_from_file, get_all_file_system_items, match_condition

log = logging.getLogger(LOGGER_NAME)

FAIL_REASON = "These tests are failed because of removing 'helperFolding' and 'deadCodeRemoval' from transformations."


BASE_DATA_PATH = os.path.join(TEST_DATA_PATH, 'solution_space/')


class TEST_METHOD(Enum):
    KELLY = 'Kelly Rivers'
    GUM_TREE = 'Gum Tree Diff'


class TEST_TYPE(Enum):
    DIFF = 'diffs'


def __get_sources_and_goals(task: TASK, test_type: TEST_TYPE = TEST_TYPE.DIFF) -> Tuple[List[str], List[str]]:
    root = os.path.join(BASE_DATA_PATH, test_type.value, task.value)
    sources_paths = get_all_file_system_items(root, match_condition(r'source_\d+.py'))
    sources_paths.sort()
    goals_paths = get_all_file_system_items(root, match_condition(r'goal_\d+.py'))
    goals_paths.sort()

    sources = [get_content_from_file(f) for f in sources_paths]
    goals = [get_content_from_file(f) for f in goals_paths]
    return sources, goals


def __get_code_by_source(source: str, is_goal: bool = False) -> Code:
    anon_tree, canon_tree = get_trees(source, {TREE_TYPE.ANON, TREE_TYPE.CANON})
    rate = 0 if not is_goal else TEST_RESULT.FULL_SOLUTION.value
    return Code(canon_tree=canon_tree, rate=rate, anon_tree=anon_tree)


def get_solution_graph(task: TASK, to_plot_graph: bool = True, test_prefix: str = 'num_diffs') -> SolutionGraph:
    sources, goals = __get_sources_and_goals(task)
    sg = SolutionGraph(task)
    code_info = CodeInfo(User())
    for goal in goals:
        goal_code = __get_code_by_source(goal, is_goal=True)
        codes = [__get_code_by_source(s) for s in sources] + [goal_code]
        chain = [(code, code_info) for code in codes]
        sg.add_code_info_chain(chain)
    if to_plot_graph:
        path = __plot_graph(task, sg, test_prefix)
        log.info(f'Graph path for solution space for task {task.value} is {path}')
    return sg


def __plot_graph(task: TASK, sg: SolutionGraph, test_prefix: str) -> str:
    gv = SolutionSpaceVisualizer(sg)
    return gv.create_graph_representation(name_prefix=f'test_graph_{test_prefix}_{task.value}')
