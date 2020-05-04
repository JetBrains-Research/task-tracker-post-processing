# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from collections import defaultdict
from typing import Tuple, Dict, Union, List

from src.main.canonicalization.consts import TREE_TYPE
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.canonicalization.ast_tools import get_vertices_number_in_ast


def get_general_solution_graph_statistics(solution_graph: SolutionGraph) -> Tuple[Dict[int, int], Dict[int, int]]:
    canon_trees_freqs = defaultdict(int)
    anon_trees_freqs = defaultdict(int)

    vertices = solution_graph.get_traversal()
    vertices.remove(solution_graph.start_vertex)
    for vertex in vertices:
        vertices_number = get_vertices_number_in_ast(vertex.serialized_code.canon_tree)
        canon_trees_freqs[vertices_number] += 1
        for anon_tree in vertex.serialized_code.anon_trees:
            vertices_number = get_vertices_number_in_ast(anon_tree)
            anon_trees_freqs[vertices_number] += 1
    return canon_trees_freqs, anon_trees_freqs


def __get_default_dict_for_vertex() -> dict:
    return {
        TREE_TYPE.CANON: 0,
        TREE_TYPE.ANON: []
    }


def get_statistics_for_each_vertex(solution_graph: SolutionGraph) -> dict:
    statistics_dict = {}
    vertices = solution_graph.get_traversal()
    vertices.remove(solution_graph.start_vertex)
    for vertex in vertices:
        statistics_dict[vertex.id] = __get_default_dict_for_vertex()
        statistics_dict[vertex.id][TREE_TYPE.CANON] = get_vertices_number_in_ast(vertex.serialized_code.canon_tree)
        for anon_tree in vertex.serialized_code.anon_trees:
            statistics_dict[vertex.id][TREE_TYPE.ANON].append(get_vertices_number_in_ast(anon_tree))
        statistics_dict[vertex.id][TREE_TYPE.ANON].sort()
    return statistics_dict
