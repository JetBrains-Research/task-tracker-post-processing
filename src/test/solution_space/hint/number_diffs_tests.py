# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Tuple, Any, List

from src.test.test_util import LoggedTest
from src.main.util.consts import TASK, LOGGER_NAME
from src.main.util.log_util import log_and_raise_error
from src.main.canonicalization.diffs.diff_handler import DiffHandler
from src.main.solution_space.solution_graph import Vertex, SolutionGraph
from src.test.solution_space.hint.util import get_solution_graph, TEST_METHOD
from src.main.canonicalization.canonicalization import get_code_from_tree, ast

log = logging.getLogger(LOGGER_NAME)

DIFFS_NUMBER = 'diffs_number'
GOAL_ID = 'goal_id'

USER_CODE_1 = 'a = int(input())\nb = int(input())'

USER_CODE = [USER_CODE_1]


class PiesDiffsTypes:
    def __init__(self, diffs: Tuple[int, ...]):
        self.from_empty_to_goal, self.from_one_input_to_goal, self.from_two_inputs_to_goal, \
        self.from_three_inputs_to_goal, self.from_user_to_goal = diffs

    def __str__(self) -> str:
        return f'From empty to goal = {self.from_empty_to_goal}\nFrom one input to goal (canon or anon form) = ' \
               f'{self.from_one_input_to_goal}\n' \
               f'From two inputs to goal (canon or anon form) = {self.from_two_inputs_to_goal}\n' \
               f'From three inputs to goal (canon or anon form) = {self.from_three_inputs_to_goal}\n' \
               f'From user to goal = {self.from_user_to_goal}'


# Todo: maybe we want to add some information to goals and so we use dict
RESOURCES_FOR_TASKS = {
    TASK.PIES: {
        USER_CODE_1: [
            {
                GOAL_ID: 6
            },
            {
                GOAL_ID: 7
            }
        ]
    }
}


def get_current_goal(goal_id: int, graph: SolutionGraph) -> Vertex:
    goals = graph.end_vertex.parents
    for goal in goals:
        if goal.id == goal_id:
            return goal
    log_and_raise_error(f'Goal with id {goal_id} does not exist', log)


# Todo: add type annotation
def get_resources(task: TASK, user_code: str) -> list:
    resources = RESOURCES_FOR_TASKS.get(task, None)
    if not resources:
        log_and_raise_error(f'Resources for task {task.value} does not exist', log)
    resources = resources.get(user_code, None)
    if not resources:
        log_and_raise_error(f'Resources for user code {user_code} does not exist', log)
    return resources


def anon_trees_to_str(anon_tree_list: List[ast.AST]) -> str:
    res = ''
    for i, tree in enumerate(anon_tree_list):
        res += f'Anon tree {i}\n{get_code_from_tree(tree)}\n'
    return res


def get_res_for_current_test(task: TASK, user_code: str, goal: Vertex, actual_diffs: Any,
                     test_method: TEST_METHOD) -> str:
    res = '_____________\n'
    res += f'Test method: {test_method.value}\n'
    res += f'Current task: {task.value}\n'
    res += f'Current user source code:\n{user_code}\n\n'
    res += f'Current goal id: {goal.id}\n'
    res += f'Current goal anon code:\n{anon_trees_to_str(goal.code.anon_trees)}\n'
    res += f'Current goal canon code:\n{get_code_from_tree(goal.code.canon_tree)}\n\n'
    res += f'Diffs:\n{actual_diffs}\n'
    res += '_____________\n'
    return res


def get_diffs_from_graph(graph: SolutionGraph, goal: Vertex) -> Tuple[int, ...]:
    vertices = graph.get_traversal()
    vertices.remove(graph.start_vertex)

    diffs = ()

    for vertex in vertices:
        if vertex.code.is_full():
            continue
        diffs += (graph.get_diffs_number_between_vertexes(vertex, goal),)

    return diffs


def run_kelly_rivers_test(self, task: TASK):
    s_g = get_solution_graph(task)

    for user_source_code in USER_CODE:
        resources = get_resources(task, user_source_code)
        user_diff_handler = DiffHandler(user_source_code)

        for resource in resources:
            current_goal_id = resource.get(GOAL_ID)
            goal = get_current_goal(current_goal_id, s_g)

            diffs = get_diffs_from_graph(s_g, goal)
            from_user_to_goal = goal.get_diffs_number(user_diff_handler)
            diffs += (from_user_to_goal,)

            diffs_number_res = PiesDiffsTypes(diffs)
            res = get_res_for_current_test(task, user_source_code, goal, diffs_number_res, TEST_METHOD.KELLY)
            # Todo: write to file
            log.info(res)


class TestNumberDiffs(LoggedTest):

    def test_kelly_rivers_diffs(self) -> None:
        run_kelly_rivers_test(self, TASK.PIES)