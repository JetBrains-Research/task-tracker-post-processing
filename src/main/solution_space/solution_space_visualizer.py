# Copyright (c) by anonymous author(s)

import os
from typing import Set, Dict, List

from src.main.plots.util.graph_representation_util import get_graph_representation, create_dot_graph
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
            info += f'Anon code {i}:\n{get_code_from_tree(a_t.tree)}\n'
        return info

    def __get_labels(self) -> str:
        labels = ''
        for vertex in self._graph.get_traversal():
            if self._graph.is_empty_vertex(vertex):
                labels += f'{vertex.id} [label="Vertex {vertex.id}. Empty vertex"]\n'
            else:
                labels += f'{vertex.id} [label="Vertex {vertex.id}"]\n'

        labels += f'{self._graph.end_vertex.id} [label="Vertex {self._graph.end_vertex.id}. End vertex"]\n'
        return labels

    def __create_vertices_content(self, folder_path: str) -> None:
        for vertex in self._graph.get_traversal():
            current_path = os.path.join(folder_path, f'vertex_{vertex.id}{consts.EXTENSION.TXT.value}')
            content = self.__class__.__get_vertex_info(vertex)
            create_file(content, current_path)

    @staticmethod
    def __get_vertices_list(vertices: List[Vertex]) -> str:
        vertices = list(set(map(lambda v: v.id, vertices)))
        vertices.sort()
        return ', '.join(list(map(str, vertices)))

    def __get_graph_representation(self, font_name: str = 'Arial') -> str:
        return get_graph_representation(self.__get_labels(), self.__get_graph_structure(), font_name)

    def __get_graph_structure(self) -> str:
        structure = ''
        for vertex in self._graph.get_traversal():
            if vertex.children:
                structure += f'{vertex.id} -> {self.__class__.__get_vertices_list(vertex.children)}\n'
        return structure

    # Returns result's folder path
    def visualize_graph(self, name_prefix: str = 'graph',
                        to_create_vertices_content: bool = True,
                        output_format: consts.EXTENSION = consts.EXTENSION.PNG) -> str:
        graph_representation = self.__get_graph_representation()
        folder_path = os.path.join(consts.GRAPH_REPRESENTATION_PATH, f'{name_prefix}_{self._graph.id}')
        # Remove older graph with the same name
        remove_directory(folder_path)
        create_dot_graph(folder_path, name_prefix, graph_representation, output_format)
        if to_create_vertices_content:
            self.__create_vertices_content(folder_path)
        return folder_path
