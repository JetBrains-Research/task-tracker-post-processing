# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Tuple, Dict
from collections import defaultdict

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
