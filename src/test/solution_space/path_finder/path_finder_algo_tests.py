# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

from src.main.util.consts import TASK, LOGGER_NAME
from src.test.solution_space.path_finder.util import get_solution_graph, get_user_solutions

log = logging.getLogger(LOGGER_NAME)


def run_test(task: TASK, test_prefix: str) -> None:
    sg = get_solution_graph(task, test_prefix=test_prefix)
    user_solutions = get_user_solutions(task)
    # Todo: run path finder algo and write result to the file
    pass
