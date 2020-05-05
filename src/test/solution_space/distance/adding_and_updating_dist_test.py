# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import itertools
import collections
from enum import Enum
from typing import Dict, List, Tuple

import pytest
import numpy as np

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.canonicalization.consts import TREE_TYPE
from src.main.solution_space.serialized_code import Code
from src.main.canonicalization.diffs.gumtree import GumTreeDiff
from src.main.solution_space.data_classes import CodeInfo, User
from src.main.util.consts import TASK, LOGGER_NAME, TEST_RESULT
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.consts import SOLUTION_SPACE_TEST_FOLDER
from src.main.canonicalization.canonicalization import get_trees, are_asts_equal

log = logging.getLogger(LOGGER_NAME)

SolutionGraph.solution_space_folder = SOLUTION_SPACE_TEST_FOLDER


# For testing, we have 6 different fragments, and some of them have the same canon tree, which form 3 vertices.
class VERTEX(Enum):
    VERTEX_0 = 'vertex_0'
    VERTEX_1 = 'vertex_1'
    VERTEX_2 = 'vertex_2'


# For each vertex we will store indices of fragments, that belong to it.
# Fragments with the same canon tree for the vertex_0:
fragment_0 = "a = 5\n" \
             "if a < 6:\n" \
             "    print(a)"

fragment_1 = "five = 5\n" \
             "if 6 > five:\n" \
             "    print(5)"

fragment_2 = "c = 4 + 1\n" \
             "if c < (7 - 1):\n" \
             "    print(4+1)"

vertex_0_indices = [0, 1, 2]

# Fragments with the same canon tree for the vertex_1:
fragment_3 = "a = int(input())\n" \
             "c = 5\n" \
             "print((a + b)*6)"

fragment_4 = "a = int(input())\n" \
             "c = 1 + 1 + 1 + 1 + 1\n" \
             "print(6*(a + b))"

vertex_1_indices = [3, 4]

# Fragment for the vertex_2:
fragment_5 = "a = int(input())\n" \
             "b = int(input())"

vertex_2_indices = [5]

all_fragments = [fragment_0, fragment_1, fragment_2, fragment_3, fragment_4, fragment_5]

# For each vertex we store indices of fragments (according to all_fragments list), which belong to this vertex:
INDICES_BY_VERTEX = {VERTEX.VERTEX_0: vertex_0_indices,
                     VERTEX.VERTEX_1: vertex_1_indices,
                     VERTEX.VERTEX_2: vertex_2_indices}


def get_vertex_by_index(index: 0) -> VERTEX:
    for vertex in INDICES_BY_VERTEX.keys():
        if index in INDICES_BY_VERTEX[vertex]:
            return vertex
    raise ValueError(f'No vertices found for given index {index}')


# Distances between all anon trees for all 6 fragments:
# (Seems GumTreeDiff distance is not commutative :c )
anon_distance = [[0, 8, 12, 20, 33, 21],
                 [8, 0, 16, 20, 30, 21],
                 [12, 16, 0, 28, 38, 27],
                 [20, 20, 28, 0, 11, 16],
                 [33, 33, 38, 11, 0, 24],
                 [24, 21, 27, 16, 24, 0]]

# Distances between all canon trees for all 3 vertices:
canon_distance = {VERTEX.VERTEX_0: {VERTEX.VERTEX_0: 0, VERTEX.VERTEX_1: 12, VERTEX.VERTEX_2: 4},
                  VERTEX.VERTEX_1: {VERTEX.VERTEX_0: 12, VERTEX.VERTEX_1: 0, VERTEX.VERTEX_2: 14},
                  VERTEX.VERTEX_2: {VERTEX.VERTEX_0: 4, VERTEX.VERTEX_1: 14, VERTEX.VERTEX_2: 0}}

# If we add fragments to the solution graph in that order, vertices will be created or updated like this:
#  *adding fragment_0*  vertex_0 created
#  *adding fragment_3*  vertex_1 created
#  *adding fragment_1*  vertex_0 updated
#  *adding fragment_5*  vertex_2 created
#  *adding fragment_2*  vertex_0 updated
#  *adding fragment_4*  vertex_1 updated
fragment_indices_to_add = [0, 3, 1, 5, 2, 4]


# Finds distance matrix between all vertices in given dict, using anon trees which indices listed in the dict.
#
# For example, for added_indices_by_vertex: {VERTEX.VERTEX_0: [0, 3],
#                                            VERTEX.VERTEX_1: [4]}
# it will find all distances between
# 1. VERTEX_0 with fragment_0, fragment_3
# 2. VERTEX_1 with fragment_4.
#
# It's useful for finding intermediate distance matrix while adding new fragments.
def find_dist_matrix(added_indices_by_vertex: Dict[VERTEX, List[int]]) -> List[List[int]]:
    dist_matrix = []
    for i, src_vertex in enumerate(added_indices_by_vertex.keys()):
        dist_matrix.append([])
        src_indices = added_indices_by_vertex[src_vertex]
        for j, dst_vertex in enumerate(added_indices_by_vertex.keys()):
            dst_indices = added_indices_by_vertex[dst_vertex]
            canon_dist = canon_distance[src_vertex][dst_vertex]
            anon_dist = min([anon_distance[k][l] for k in src_indices for l in dst_indices])
            dist_matrix[i].append(min(anon_dist, canon_dist))
    return dist_matrix


def get_code_info_chain(sources: List[str]) -> List[Tuple[Code, CodeInfo]]:
    user = User()
    return [(Code.from_source(s, TEST_RESULT.CORRECT_CODE.value), CodeInfo(user)) for s in sources]


@pytest.mark.skip(reason='We don\'t use dist in solution graph anymore')
class TestDistBetweenVertices:

    # Check all fragments in same vertices have the same canon trees
    @pytest.mark.parametrize('vertex', [v for v in VERTEX])
    def test_same_canon_trees_in_same_vertices(self, vertex: VERTEX, subtests):
        same_canon_fragments = [all_fragments[i] for i in INDICES_BY_VERTEX[vertex]]
        canon_trees = [get_trees(f, {TREE_TYPE.CANON})[0] for f in same_canon_fragments]
        for canon_tree_1, canon_tree_2 in itertools.product(canon_trees, repeat=2):
            with subtests.test():
                assert are_asts_equal(canon_tree_1, canon_tree_2)

    # Check all fragments in different vertices have different canon trees
    def test_different_canon_trees_in_different_vertices(self, subtests):
        # Take the first fragment from each vertex to get all fragments with different canon trees
        different_canon_fragments = [all_fragments[INDICES_BY_VERTEX[vertex][0]] for vertex in VERTEX]
        canon_trees = [get_trees(f, {TREE_TYPE.CANON})[0] for f in different_canon_fragments]
        for canon_tree_1, canon_tree_2 in zip(canon_trees, np.roll(canon_trees, 1)):
            with subtests.test():
                assert not are_asts_equal(canon_tree_1, canon_tree_2)

    # Check anon distance matrix is filled right
    def test_anon_distance_correctness(self, subtests):
        fragments = [fragment_0, fragment_1, fragment_2, fragment_3, fragment_4, fragment_5]
        for i, src_fragment in enumerate(fragments):
            src_anon_tree, = get_trees(src_fragment, {TREE_TYPE.ANON})
            for j, dst_fragment in enumerate(fragments):
                with subtests.test():
                    dst_anon_tree, = get_trees(dst_fragment, {TREE_TYPE.ANON})
                    real_dist = GumTreeDiff.create_tmp_files_and_get_diffs_number(src_anon_tree, dst_anon_tree)
                    assert real_dist == anon_distance[i][j], f'Dists are not equal: {i}, {j}'

    # Check canon distance matrix is filled right
    @pytest.mark.parametrize('src_vertex', [v for v in VERTEX])
    def test_canon_distance_correctness(self, src_vertex, subtests):
        src_canon_tree, = get_trees(all_fragments[INDICES_BY_VERTEX[src_vertex][0]], {TREE_TYPE.CANON})
        for dst_vertex in VERTEX:
            with subtests.test():
                dst_canon_tree, = get_trees(all_fragments[INDICES_BY_VERTEX[dst_vertex][0]], {TREE_TYPE.CANON})
                real_dist = GumTreeDiff.create_tmp_files_and_get_diffs_number(src_canon_tree, dst_canon_tree)
                assert real_dist == canon_distance[src_vertex][dst_vertex]

    def test_consequent_dist_updating(self, subtests):
        sg = SolutionGraph(TASK.PIES)
        added_indices_by_vertex = collections.defaultdict(list)
        for i in fragment_indices_to_add:
            with subtests.test():
                # We should create code_info_chain for each fragment to emulate consequent fragments adding.
                code_info_chain = get_code_info_chain([all_fragments[i]])
                sg.add_code_info_chain(code_info_chain)
                actual_dist_matrix = sg._dist._IDistanceMatrix__get_dist_matrix()

                added_indices_by_vertex[get_vertex_by_index(i)].append(i)
                expected_dist_matrix = find_dist_matrix(added_indices_by_vertex)

                assert expected_dist_matrix == actual_dist_matrix
