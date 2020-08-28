# Copyright (c) by anonymous author(s)

import logging
from enum import Enum
from typing import List, Tuple, Dict, Union

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.solution_space.serialized_code import Code
from src.main.util.consts import TEST_RESULT, LOGGER_NAME, TASK
from src.main.solution_space.data_classes import User, CodeInfo
from src.main.solution_space.consts import SOLUTION_SPACE_TEST_FOLDER
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.test.solution_space.solution_graph.util import init_default_ids
from src.main.canonicalization.canonicalization import get_code_from_tree

log = logging.getLogger(LOGGER_NAME)


CURRENT_TASK = TASK.PIES
SolutionGraph.solution_space_folder = SOLUTION_SPACE_TEST_FOLDER


class ADJACENT_VERTEX_TYPE(Enum):
    CHILDREN = 'children'
    PARENTS = 'parents'


class VERTEX_STRUCTURE(Enum):
    CODE_INFO_LIST_LEN = 'users_number'
    SOURCE = 'source'


VertexStructure = Dict[VERTEX_STRUCTURE, Union[str, int]]


def create_graph_with_code() -> (SolutionGraph, List[Vertex], List[str], List[float]):
    empty_source = ''
    source_0 = 'print(\'Hello\')'
    source_1 = 'a = int(input())\nprint(a)'
    source_2 = 'x = 5\nif(x > 4):\n    print(x)'

    sources = [source_0, source_1, source_2]

    sg = SolutionGraph(CURRENT_TASK)
    #           START_VERTEX
    #         /             \
    #  empty vertex       vertex_0
    #         |           /    \
    #      vertex_1     /   END_VERTEX
    #           \     /
    #           vertex_2

    # Vertex_1 has to have a full_solution code since this vertex is connected with end_vertex
    rates = [TEST_RESULT.FULL_SOLUTION.value, TEST_RESULT.CORRECT_CODE.value, TEST_RESULT.CORRECT_CODE.value]

    vertices = [Vertex(sg, code=Code.from_source(s, rates[i])) for i, s in enumerate(sources)]

    # Add code infos with different users
    list(map(lambda v: v.serialized_code.anon_trees[0].add_code_info(CodeInfo(User())), vertices))

    sg.connect_to_start_vertex(vertices[0])

    sg.empty_vertex.add_child(vertices[1])
    vertices[0].add_child(vertices[2])
    vertices[1].add_child(vertices[2])

    sg.connect_to_end_vertex(vertices[0])

    return sg, [sg.empty_vertex] + vertices, [empty_source] + sources, [TEST_RESULT.CORRECT_CODE.value] + rates


def find_or_create_vertex_with_code_info_and_rate_check(sg: SolutionGraph, source: str,
                                                        rate: float = TEST_RESULT.CORRECT_CODE.value) -> Vertex:
    code_info = CodeInfo(User())
    code = Code.from_source(source, rate)
    found_vertex = sg.find_or_create_vertex(code, code_info)
    # Check if user is added to user list
    assert code_info in found_vertex.serialized_code.find_anon_tree(code.anon_tree).code_info_list
    # Check if vertex is connected with end_vertex if it has 'full_solution'-code
    if rate == TEST_RESULT.FULL_SOLUTION.value:
        assert sg.end_vertex in found_vertex.children
    return found_vertex


def create_code_info_chain() -> (List[Tuple[Code, CodeInfo]], List[str]):
    source_1 = 'a = 3\nprint(a)'
    source_2 = 'a = int(input())\nprint(a)'
    source_3 = 'a = 5\nb = 3\nprint(a - b)'
    source_4 = 'a = 5\nb = 3\nc = 4\nprint(a - b - c)'
    rated_sources = [(source_1, TEST_RESULT.CORRECT_CODE.value),
                     (source_2, TEST_RESULT.CORRECT_CODE.value),
                     (source_3, TEST_RESULT.CORRECT_CODE.value),
                     (source_4, TEST_RESULT.FULL_SOLUTION.value)]
    # User is the same for all chain elements
    user = User()
    chain = [(Code.from_source(s, r), CodeInfo(user)) for s, r in rated_sources]
    canon_sources = [get_code_from_tree(code.canon_tree).rstrip('\n') for code, _ in chain]
    return chain, canon_sources


def get_vertex_structure(vertex: Vertex) -> VertexStructure:
    source = get_code_from_tree(vertex.serialized_code.canon_tree).strip('\n') if vertex.serialized_code else None
    code_info_list_len = 0 if vertex.serialized_code is None \
        else sum([len(a_t.code_info_list) for a_t in vertex.serialized_code.anon_trees])
    return {VERTEX_STRUCTURE.SOURCE: source, VERTEX_STRUCTURE.CODE_INFO_LIST_LEN: code_info_list_len}


def check_adjacent_vertices_structure(adjacent_vertex_type: ADJACENT_VERTEX_TYPE, vertex: Vertex,
                                      adjacent_vertices_structure: List[VertexStructure]) -> None:
    adjacent_vertices = getattr(vertex, adjacent_vertex_type.value, [])
    assert len(adjacent_vertices) == len(adjacent_vertices_structure)

    for adjacent_vertex in adjacent_vertices:
        real_structure = get_vertex_structure(adjacent_vertex)
        assert real_structure in adjacent_vertices_structure
        adjacent_vertices_structure.remove(real_structure)

    # Check if empty
    assert not adjacent_vertices_structure


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestGraph:

    def test_bfs_traversal(self) -> None:
        init_default_ids()
        # A simple graph without any code just to check bfs
        sg = SolutionGraph(CURRENT_TASK)
        #               START_VERTEX
        #               |          \
        #            vertex_1     empty_vertex
        #          /    |     \
        # vertex_2   vertex_3   vertex_4
        #       \    /      \    /
        #       vertex_5    vertex_6
        #                      |
        #                  END_VERTEX
        vertex_1 = Vertex(sg)
        sg.connect_to_start_vertex(vertex_1)

        vertex_2, vertex_3, vertex_4 = Vertex(sg), Vertex(sg), Vertex(sg)
        vertex_1.add_child(vertex_2)
        vertex_1.add_child(vertex_3)
        vertex_1.add_child(vertex_4)

        vertex_5, vertex_6 = Vertex(sg), Vertex(sg)
        vertex_2.add_child(vertex_5)
        vertex_3.add_child(vertex_5)
        vertex_3.add_child(vertex_6)
        vertex_4.add_child(vertex_6)

        sg.connect_to_end_vertex(vertex_6)
        # With start_vertex, but without end_vertex
        expected_traversal = [sg.start_vertex, sg.empty_vertex, vertex_1, vertex_2, vertex_3, vertex_4, vertex_5, vertex_6]
        actual_traversal = sg.get_traversal(to_remove_start=False)
        assert actual_traversal == expected_traversal

    def test_finding_vertex(self) -> None:
        init_default_ids()
        sg, vertices, sources, rates = create_graph_with_code()
        for i, vertex in enumerate(vertices):
            found_vertex = find_or_create_vertex_with_code_info_and_rate_check(sg, sources[i], rates[i])
            assert found_vertex == vertex

    def test_creating_vertex(self) -> None:
        init_default_ids()
        sg, vertices, sources, _ = create_graph_with_code()
        source = 'while(True):\n    print(\'Hi\')'
        found_vertex = find_or_create_vertex_with_code_info_and_rate_check(sg, source, TEST_RESULT.FULL_SOLUTION.value)
        assert found_vertex not in vertices

    def test_finding_or_creating_vertex_with_none(self) -> None:
        init_default_ids()
        sg, vertices, sources, _ = create_graph_with_code()
        user = User()
        with pytest.raises(ValueError):
            sg.find_or_create_vertex(None, CodeInfo(user=user))

    def test_adding_code_info_chain(self) -> None:
        init_default_ids()
        sg, vertices, vertex_sources, _ = create_graph_with_code()

        # Graph with code:
        #
        #           START_VERTEX
        #         /             \
        #     empty_vertex       vertex_1
        #         |           /    \
        #      vertex_2     /   END_VERTEX
        #           \     /
        #           vertex_3

        chain, chain_sources = create_code_info_chain()
        sg.add_code_info_chain(chain)
        # Graph with code and the added chain:
        #
        #                   START_VERTEX
        #               /      |          \
        #         chain_0  empty_vertex  vertex_1
        #              |       |          /    |
        #       [chain_1, vertex_2]      /     /
        #               \       \       /     /
        #             chain_2    vertex_3    /
        #                   \               /
        #                   chain_3        /
        #                        \        /
        #                       END_VERTEX

        # Since new vertices for the chain were created, we cannot compare them to any existed vertices for checking,
        # but we can check children and parents structure (source and code infos len) of the known old vertices

        # We can find the structure of the known old vertices:
        vertex_0_structure = get_vertex_structure(vertices[0])
        vertex_1_structure = get_vertex_structure(vertices[1])
        vertex_2_structure = get_vertex_structure(vertices[2])
        vertex_3_structure = get_vertex_structure(vertices[3])

        start_vertex_structure = get_vertex_structure(sg.start_vertex)
        end_vertex_structure = get_vertex_structure(sg.end_vertex)

        # Also, the structure of the new chain vertices should be like that:
        chain_0_structure = {VERTEX_STRUCTURE.SOURCE: chain_sources[0],
                             VERTEX_STRUCTURE.CODE_INFO_LIST_LEN: 1}
        chain_1_structure = {VERTEX_STRUCTURE.SOURCE: chain_sources[1],
                             VERTEX_STRUCTURE.CODE_INFO_LIST_LEN: 2}
        chain_2_structure = {VERTEX_STRUCTURE.SOURCE: chain_sources[2],
                             VERTEX_STRUCTURE.CODE_INFO_LIST_LEN: 1}
        chain_3_structure = {VERTEX_STRUCTURE.SOURCE: chain_sources[3],
                             VERTEX_STRUCTURE.CODE_INFO_LIST_LEN: 1}

        # We should have 1 joined vertex: [chain_1, vertex_2] with the same structure:
        assert chain_1_structure == vertex_2_structure

        # Now we can check that each of the old known vertices
        # has the right children and parents structure and their amount:
        # START_VERTEX has 3 children: chain_0, vertex_0 and vertex_1; no parents
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.CHILDREN, sg.start_vertex,
                                          [chain_0_structure, vertex_0_structure, vertex_1_structure])
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.PARENTS, sg.start_vertex, [])

        # vertex_0 has 1 child: [chain_1, vertex_2]; 1 parent: START_VERTEX
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.CHILDREN, vertices[0], [chain_1_structure])
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.PARENTS, vertices[0], [start_vertex_structure])

        # vertex_1 has 2 children: vertex_3 and END_VERTEX; 1 parent: START_VERTEX
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.CHILDREN, vertices[1],
                                          [vertex_3_structure, end_vertex_structure])
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.PARENTS, vertices[1], [start_vertex_structure])

        # vertex_2 has 2 children: vertex_3 and chain_2; 2 parents: vertex_0 and chain_0
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.CHILDREN, vertices[2],
                                          [vertex_3_structure, chain_2_structure])
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.PARENTS, vertices[2],
                                          [vertex_0_structure, chain_0_structure])

        # vertex_3 has no children and 2 parents: [chain_1, vertex_2] and vertex_1
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.CHILDREN, vertices[3], [])
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.PARENTS, vertices[3],
                                          [vertex_2_structure, vertex_1_structure])

        # END_VERTEX has no children and 2 parents: chain_3 and vertex_1
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.CHILDREN, sg.end_vertex, [])
        check_adjacent_vertices_structure(ADJACENT_VERTEX_TYPE.PARENTS, sg.end_vertex,
                                          [chain_3_structure, vertex_1_structure])
