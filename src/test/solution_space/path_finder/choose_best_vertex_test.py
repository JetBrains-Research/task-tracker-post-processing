# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from typing import Optional

import pytest

from src.main.solution_space.serialized_code import Code
from src.test.util import to_skip, TEST_LEVEL
from src.main.util.consts import TEST_DATA_PATH, TASK
from src.main.canonicalization.consts import TREE_TYPE
from src.main.util.file_util import get_content_from_file
from src.main.solution_space.data_classes import Profile, User
from src.main.canonicalization.canonicalization import get_trees
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.test.solution_space.solution_graph.util import get_two_vertices
from src.main.solution_space.path_finder.path_finder_v_1 import PathFinderV1

USER_SOURCE_PATH = os.path.join(TEST_DATA_PATH, 'solution_space', 'choose_best_vertex', 'source.py')
USER_SOURCE = get_content_from_file(USER_SOURCE_PATH)
USER_ANON_AST, USER_CANON_AST = get_trees(USER_SOURCE, {TREE_TYPE.ANON, TREE_TYPE.CANON})

USER_CODE = Code(USER_CANON_AST, 1, USER_ANON_AST)
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
PF = PathFinderV1(SG)


def get_best_vertex_from_empty_list() -> Optional[Vertex]:
    # Call the private function
    return PF._PathFinderV1__choose_best_vertex(USER_CODE, DEFAULT_USER, [])


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestChooseBestVertexMethod:

    def test_empty_list(self) -> None:
        assert get_best_vertex_from_empty_list() is None

    # Todo: add tests
