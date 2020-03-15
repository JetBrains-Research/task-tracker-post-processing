import ast
import logging
import unittest
from enum import Enum
from typing import List, Tuple

from src.main.solution_space.data_classes import Code, User
from src.main.solution_space.solution_graph import Vertex, SolutionGraph
from src.main.canonicalization.canonicalization import get_code_from_tree
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT, TEST_RESULT, LOGGER_NAME

log = logging.getLogger(LOGGER_NAME)


class ADJACENT_VERTEX_TYPE(Enum):
    CHILDREN = 'children'
    PARENTS = 'parents'


class VERTEX_STRUCTURE(Enum):
    USERS_NUMBER = 'users_number'
    SOURCE = 'source'


def create_code_from_source(source: str, rate=TEST_RESULT.CORRECT_CODE.value) -> Code:
    return Code(ast.parse(source), rate)


def create_graph_with_code() -> (SolutionGraph, List[Vertex], List[str]):
    source_0 = ''
    source_1 = 'print(\'Hello\')'
    source_2 = 'a = 5'
    source_3 = 'x = True\nif(x):\n    x = False'

    sources = [source_0, source_1, source_2, source_3]

    sg = SolutionGraph()
    #           START_VERTEX
    #         /             \
    #      vertex_0       vertex_1
    #         |           /    \
    #      vertex_2     /   END_VERTEX
    #           \     /
    #           vertex_3

    # vertex_1 has to have a full_solution code since this vertex is connected with end_vertex
    rates = [TEST_RESULT.CORRECT_CODE.value, TEST_RESULT.FULL_SOLUTION.value, TEST_RESULT.CORRECT_CODE.value, TEST_RESULT.CORRECT_CODE.value]
    vertices = [Vertex(create_code_from_source(s, rates[i])) for i, s in enumerate(sources)]
    list(map(lambda v: v.add_user(User()), vertices))

    sg.connect_to_start_vertex(vertices[0])
    sg.connect_to_start_vertex(vertices[1])

    vertices[0].add_child(vertices[2])
    vertices[1].add_child(vertices[3])
    vertices[2].add_child(vertices[3])

    sg.connect_to_end_vertex(vertices[1])

    return sg, vertices, sources


def find_or_create_vertex_with_user_and_rate_check(self: unittest.TestCase, sg: SolutionGraph, source: str,
                                                   rate=TEST_RESULT.CORRECT_CODE.value) -> Vertex:
    user = User()
    found_vertex = sg.find_or_create_vertex(create_code_from_source(source, rate), user)
    # check if user is added to user list
    self.assertTrue(user in found_vertex.users)
    # check if vertex is connected with end_vertex if it has 'full_solution'-code
    if rate == TEST_RESULT.FULL_SOLUTION.value:
        self.assertTrue(sg.end_vertex in found_vertex.children)
    return found_vertex


def create_code_user_chain() -> (List[Tuple[Code, User]], List[str]):
    source_1 = 'a = 3'
    source_2 = 'a = 5'
    source_3 = 'a = 5\nb = 3'
    source_4 = 'a = 5\nb = 3\nc = 4'
    rated_sources = [(source_1, TEST_RESULT.CORRECT_CODE.value),
                     (source_2, TEST_RESULT.CORRECT_CODE.value),
                     (source_3, TEST_RESULT.CORRECT_CODE.value),
                     (source_4, TEST_RESULT.FULL_SOLUTION.value)]
    chain = [(create_code_from_source(rs[0], rs[1]), User()) for rs in rated_sources]
    sources = [rs[0] for rs in rated_sources]
    return chain, sources


def get_vertex_structure(vertex: Vertex) -> dict:
    source = get_code_from_tree(vertex.code.ast).strip('\n') if vertex.code else None
    return {VERTEX_STRUCTURE.SOURCE.value: source, VERTEX_STRUCTURE.USERS_NUMBER.value: len(vertex.users)}


def check_adjacent_vertices_structure(self: unittest.TestCase, adjacent_vertex_type: ADJACENT_VERTEX_TYPE, vertex: Vertex,
                                      adjacent_vertices_structure: List[dict]) -> None:
    adjacent_vertices = getattr(vertex, adjacent_vertex_type.value, [])
    self.assertEqual(len(adjacent_vertices), len(adjacent_vertices_structure))

    for adjacent_vertex in adjacent_vertices:
        real_structure = get_vertex_structure(adjacent_vertex)
        self.assertTrue(real_structure in adjacent_vertices_structure)
        adjacent_vertices_structure.remove(real_structure)

    # check if empty
    self.assertTrue(not adjacent_vertices_structure)


def compare_structures(structure_1, structure_2):
    sources = [s.get(VERTEX_STRUCTURE.SOURCE.value).strip('\n') for s in [structure_1, structure_2]]
    user_numbers = [s.get(VERTEX_STRUCTURE.USERS_NUMBER.value) for s in [structure_1, structure_2]]
    return sources[0] == sources[1] and user_numbers[0] == user_numbers[1]


class TestGraph(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_bfs_traversal(self):
        # a simple graph without any code just to check bfs
        sg = SolutionGraph()
        #          START_VERTEX
        #               |
        #            vertex_1
        #          /    |     \
        # vertex_2   vertex_3   vertex_4
        #       \    /      \    /
        #       vertex_5    vertex_6
        #                      |
        #                  END_VERTEX
        vertex_1 = Vertex()
        sg.connect_to_start_vertex(vertex_1)

        vertex_2, vertex_3, vertex_4 = Vertex(), Vertex(), Vertex()
        vertex_1.add_child(vertex_2)
        vertex_1.add_child(vertex_3)
        vertex_1.add_child(vertex_4)

        vertex_5, vertex_6 = Vertex(), Vertex()
        vertex_2.add_child(vertex_5)
        vertex_3.add_child(vertex_5)
        vertex_3.add_child(vertex_6)
        vertex_4.add_child(vertex_6)

        sg.connect_to_end_vertex(vertex_6)
        # with start_vertex, but without end_vertex
        expected_traversal = [sg.start_vertex, vertex_1, vertex_2, vertex_3, vertex_4, vertex_5, vertex_6]
        actual_traversal = sg.get_traversal()
        self.assertEqual(actual_traversal, expected_traversal)

    def test_finding_vertex(self):
        sg, vertices, sources = create_graph_with_code()
        for i, vertex in enumerate(vertices):
            found_vertex = find_or_create_vertex_with_user_and_rate_check(self, sg, sources[i])
            self.assertEqual(found_vertex, vertex)

    def test_creating_vertex(self):
        sg, vertices, sources = create_graph_with_code()
        source = 'while(True):\n    print(\'Hi\')'
        found_vertex = find_or_create_vertex_with_user_and_rate_check(self, sg, source, TEST_RESULT.FULL_SOLUTION.value)
        self.assertTrue(found_vertex not in vertices)

    def test_finding_or_creating_vertex_with_none(self):
        sg, vertices, sources = create_graph_with_code()
        user = User()
        self.assertRaises(ValueError, sg.find_or_create_vertex, None, user)

    def test_adding_code_user_chain(self):
        sg, vertices, vertex_sources = create_graph_with_code()

        # Graph with code:
        #
        #           START_VERTEX
        #         /             \
        #      vertex_0       vertex_1
        #         |           /    \
        #      vertex_2     /   END_VERTEX
        #           \     /
        #           vertex_3

        chain, chain_sources = create_code_user_chain()
        sg.add_code_user_chain(chain)
        # Graph with code and the added chain:
        #
        #                   START_VERTEX
        #               /      |          \
        #         chain_0    vertex_0     vertex_1
        #              |       |          /    |
        #       [chain_1, vertex_2]      /     /
        #               \       \       /     /
        #             chain_2    vertex_3    /
        #                   \               /
        #                   chain_3        /
        #                        \        /
        #                       END_VERTEX

        # since new vertices for the chain were created, we cannot compare them to any existed vertices for checking,
        # but we can check children and parents structure (source and users number) of the known old vertices

        # We can find the structure of the known old vertices:
        vertex_0_structure = get_vertex_structure(vertices[0])
        vertex_1_structure = get_vertex_structure(vertices[1])
        vertex_2_structure = get_vertex_structure(vertices[2])
        vertex_3_structure = get_vertex_structure(vertices[3])

        start_vertex_structure = get_vertex_structure(sg.start_vertex)
        end_vertex_structure = get_vertex_structure(sg.end_vertex)

        # Also, the structure of the new chain vertices should be like that:
        chain_0_structure = {VERTEX_STRUCTURE.SOURCE.value: chain_sources[0], VERTEX_STRUCTURE.USERS_NUMBER.value: 1}
        chain_1_structure = {VERTEX_STRUCTURE.SOURCE.value: chain_sources[1], VERTEX_STRUCTURE.USERS_NUMBER.value: 2}
        chain_2_structure = {VERTEX_STRUCTURE.SOURCE.value: chain_sources[2], VERTEX_STRUCTURE.USERS_NUMBER.value: 1}
        chain_3_structure = {VERTEX_STRUCTURE.SOURCE.value: chain_sources[3], VERTEX_STRUCTURE.USERS_NUMBER.value: 1}

        # we should have 1 joined vertex: [chain_1, vertex_2] with the same structure:
        self.assertEqual(chain_1_structure, vertex_2_structure)

        # Now we can check that each of the old known vertices has the right children and parents structure and amount:
        # START_VERTEX has 3 children: chain_0, vertex_0 and vertex_1; no parents
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.CHILDREN, sg.start_vertex, [chain_0_structure, vertex_0_structure, vertex_1_structure])
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.PARENTS, sg.start_vertex, [])

        # vertex_0 has 1 child: [chain_1, vertex_2]; 1 parent: START_VERTEX
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.CHILDREN, vertices[0], [chain_1_structure])
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.PARENTS, vertices[0], [start_vertex_structure])

        # vertex_1 has 2 children: vertex_3 and END_VERTEX; 1 parent: START_VERTEX
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.CHILDREN, vertices[1], [vertex_3_structure, end_vertex_structure])
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.PARENTS, vertices[1], [start_vertex_structure])

        # vertex_2 has 2 children: vertex_3 and chain_2; 2 parents: vertex_0 and chain_0
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.CHILDREN, vertices[2], [vertex_3_structure, chain_2_structure])
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.PARENTS, vertices[2], [vertex_0_structure, chain_0_structure])

        # vertex_3 has no children and 2 parents: [chain_1, vertex_2] and vertex_1
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.CHILDREN, vertices[3], [])
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.PARENTS, vertices[3], [vertex_2_structure, vertex_1_structure])

        # END_VERTEX has no children and 2 parents: chain_3 and vertex_1
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.CHILDREN, sg.end_vertex, [])
        check_adjacent_vertices_structure(self, ADJACENT_VERTEX_TYPE.PARENTS, sg.end_vertex, [chain_3_structure, vertex_1_structure])
