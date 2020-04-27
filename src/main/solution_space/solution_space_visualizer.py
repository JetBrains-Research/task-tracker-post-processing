# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from typing import Set, Dict, List

from src.main.util import consts
from src.main.splitting.task_checker import check_call_safely
from src.main.util.file_util import create_file, remove_directory
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.canonicalization.canonicalization import get_code_from_tree


# It is the class for creating a solution graph representation by using graphviz library
class SolutionSpaceVisualizer:
    def __init__(self, graph: SolutionGraph):
        self._graph = graph

    @staticmethod
    def __get_vertex_info(vertex: Vertex) -> str:
        info = ''
        info += f'Canon code:\n{get_code_from_tree(vertex.serialized_code.canon_tree)}\n\n'
        for i, a_t in enumerate(vertex.serialized_code.anon_trees):
            info += f'Anon code {i}:\n{get_code_from_tree(a_t)}\n'
        return info

    def __get_labels(self) -> str:
        labels = ''
        vertices = self._graph.get_traversal()
        vertices.remove(self._graph.start_vertex)
        for vertex in vertices:
            labels += f'{vertex.id} [label="Vertex {vertex.id}"]\n'

        labels += f'{self._graph.end_vertex.id} [label="Vertex {self._graph.end_vertex.id}. End vertex"]\n'
        return labels

    def __create_vertices_content(self, folder_path: str) -> None:
        vertices = self._graph.get_traversal()
        vertices.remove(self._graph.start_vertex)
        for vertex in vertices:
            current_path = os.path.join(folder_path, f'vertex_{vertex.id}{consts.EXTENSION.TXT.value}')
            content = self.__class__.__get_vertex_info(vertex)
            create_file(content, current_path)

    @staticmethod
    def __get_vertices_list(vertices: List[Vertex]) -> str:
        vertices = list(set(map(lambda v: v.id, vertices)))
        vertices.sort()
        return ', '.join(list(map(str, vertices)))

    def __get_graph_structure(self) -> str:
        structure = ''
        vertices = self._graph.get_traversal()
        vertices.remove(self._graph.start_vertex)
        for vertex in vertices:
            if vertex.children:
                structure += f'{vertex.id} -> {self.__class__.__get_vertices_list(vertex.children)}\n'
        return structure

    # We want to get a graph representation in the dot format for the graphviz library
    #
    # A simple example is:
    #
    # digraph D {
    #
    #  node [shape=record fontname=Arial];
    #
    #   A [label = "Vertex A"]
    #   B [label = "Vertex B"]
    #   C [label = "Vertex C"]
    #   D [label = "Vertex D"]
    #   F [label = "Vertex F"]
    #
    #   A -> B, C, D
    #   B -> F
    #
    # }
    #
    # For the graph:
    #                 Vertex A
    #           /         |         \
    #       Vertex B    Vertex C   Vertex D
    #           |
    #       Vertex F
    #
    def __get_graph_representation(self, font_name: str = 'Arial') -> str:
        prefix = 'digraph  D {\n\nnode [shape=record fontname=' + font_name + '];\n\n'
        graph_representation = prefix + f'{self.__get_labels()}\n\n' + self.__get_graph_structure()
        suffix = '\n\n}'
        return graph_representation + suffix

    # Returns result's folder path
    def create_graph_representation(self, name_prefix: str = 'graph',
                                    to_create_vertices_content: bool = True,
                                    output_format: consts.EXTENSION = consts.EXTENSION.PNG) -> str:
        graph_representation = self.__get_graph_representation()
        folder_path = os.path.join(consts.GRAPH_REPRESENTATION_PATH, f'{name_prefix}_{self._graph.id}')
        # Remove older graph with the same name
        remove_directory(folder_path)
        file_path = os.path.join(folder_path, f'{name_prefix}{consts.EXTENSION.DOT.value}')
        # Create dot file
        create_file(graph_representation, file_path)
        dst_path = os.path.join(folder_path, f'{name_prefix}{output_format.value}')
        args = ['dot', f'-T{output_format.value[1:]}', file_path, '-o', dst_path]
        # Generate graph representation
        check_call_safely(args)
        if to_create_vertices_content:
            self.__create_vertices_content(folder_path)
        return folder_path
