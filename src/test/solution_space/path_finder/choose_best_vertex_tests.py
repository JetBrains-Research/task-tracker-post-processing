# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
import unittest

from typing import List, Optional
from src.main.canonicalization.canonicalization import get_canonicalized_form
from src.main.solution_space.data_classes import Code, Profile, User
from src.main.solution_space.path_finder import PathFinder
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT, TEST_DATA_PATH, TASK
from src.main.util.file_util import get_content_from_file
from src.test.solution_space.solution_graph.util import get_two_vertices

USER_SOURCE_PATH = os.path.join(TEST_DATA_PATH, 'solution_space', 'choose_best_vertex', 'source.py')
USER_SOURCE = get_content_from_file(USER_SOURCE_PATH)
USER_AST = get_canonicalized_form(USER_SOURCE)

USER_CODE = Code(USER_AST, 1, USER_SOURCE_PATH)
DEFAULT_PROFILE = Profile()
DEFAULT_USER = User(DEFAULT_PROFILE)

CURRENT_TASK = TASK.PIES


def init_graph() -> SolutionGraph:
    sg = SolutionGraph(CURRENT_TASK)
    vertices = get_two_vertices(sg)
    for v in vertices:
        sg.connect_to_start_vertex(v)
        sg.connect_to_end_vertex(v)
    return sg


SG = init_graph()
PF = PathFinder(SG)


def run_empty_list_test() -> Optional[Vertex]:
    # Call the private function
    return PF._PathFinder__choose_best_vertex(USER_CODE, DEFAULT_USER, [])


class TestChooseBestVertexMethod(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_empty_list(self):
        self.assertEqual(run_empty_list_test(), None)

    # Todo: add tests