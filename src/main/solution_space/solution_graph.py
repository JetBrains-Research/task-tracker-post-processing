# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import ast
import logging
import collections
from collections import defaultdict
from typing import Optional, List, Tuple

from src.main.solution_space.vertex import Vertex
from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.serialized_code import Code
from src.main.solution_space.data_classes import CodeInfo
from src.main.util.consts import LOGGER_NAME, TASK, LANGUAGE
from src.main.util.helper_classes.id_counter import IdCounter
from src.main.solution_space.distance import VertexDistanceMatrix
from src.main.util.helper_classes.pretty_string import PrettyString
from src.main.solution_space import consts as solution_space_consts
from src.main.util.file_util import remove_directory, create_directory
from src.main.canonicalization.canonicalization import are_asts_equal, get_code_from_tree
from src.main.solution_space.consts import VERTEX_TYPE, GRAPH_FOLDER_PREFIX, SOLUTION_SPACE_FOLDER, FILE_PREFIX


log = logging.getLogger(LOGGER_NAME)


class GraphIterator(collections.abc.Iterator):
    def __init__(self, root_vertex: Vertex):
        self._root = root_vertex
        self._traversal = self.__bfs_traverse()
        self._cursor = -1

    @property
    def traversal(self) -> List[Vertex]:
        return self._traversal

    def __bfs_traverse(self) -> List[Vertex]:
        visited = [self._root]
        vertices_queue = collections.deque(visited)
        while vertices_queue:
            vertex = vertices_queue.popleft()
            for child in vertex.children:
                if child not in visited and child.vertex_type != VERTEX_TYPE.END:
                    vertices_queue.append(child)
                    visited.append(child)
        return visited

    def __next__(self):
        if self._cursor + 1 >= len(self._traversal):
            raise StopIteration
        self._cursor += 1
        return self._traversal[self._cursor]


class SolutionGraph(collections.abc.Iterable, IdCounter, PrettyString):
    solution_space_folder = SOLUTION_SPACE_FOLDER

    def __init__(self, task: TASK, language: LANGUAGE = LANGUAGE.PYTHON, to_delete_old_graph: bool = True,
                 graph_folder_prefix: str = GRAPH_FOLDER_PREFIX, file_prefix: str = FILE_PREFIX,
                 to_store_dist: bool = True):
        super().__init__()
        if language == LANGUAGE.NOT_DEFINED:
            log_and_raise_error(f'Error during constructing a solution graph. Language is not defined', log)
        self._task = task
        self._language = language

        self._graph_folder_prefix = graph_folder_prefix
        self._file_prefix = file_prefix
        self._graph_directory = self.get_default_graph_directory()

        self.canon_trees_nodes_number = defaultdict(lambda: [])
        self.anon_trees_nodes_number = defaultdict(lambda: [])

        self._start_vertex = Vertex(self, vertex_type=solution_space_consts.VERTEX_TYPE.START)
        self._end_vertex = Vertex(self, vertex_type=solution_space_consts.VERTEX_TYPE.END)

        self._dist = VertexDistanceMatrix(to_store_dist=to_store_dist)

        if to_delete_old_graph:
            remove_directory(self._graph_directory)
        create_directory(self._graph_directory)

    @property
    def graph_directory(self) -> str:
        return self._graph_directory

    @property
    def graph_folder_prefix(self) -> str:
        return self._graph_folder_prefix

    @property
    def file_prefix(self) -> str:
        return self._file_prefix

    @property
    def start_vertex(self) -> Vertex:
        return self._start_vertex

    @property
    def end_vertex(self) -> Vertex:
        return self._end_vertex

    @property
    def task(self) -> TASK:
        return self._task

    @property
    def language(self) -> LANGUAGE:
        return self._language

    def __iter__(self) -> GraphIterator:
        return GraphIterator(self._start_vertex)

    def get_traversal(self) -> List[Vertex]:
        return self.__iter__().traversal

    def get_default_graph_directory(self) -> str:
        return os.path.join(self.__class__.solution_space_folder, str(self._task.value),
                            f'{self._graph_folder_prefix}_{str(self._id)}')

    def recreate_graph_files(self, new_path_for_graph: Optional[str]) -> None:
        if new_path_for_graph is None:
            new_path_for_graph = self.get_default_graph_directory()
        self._graph_directory = new_path_for_graph

        vertices = self.get_traversal()
        vertices.remove(self.start_vertex)
        for vertex in vertices:
            vertex.serialized_code.recreate_files_for_trees(self._graph_directory)

    # Todo: add tests
    @staticmethod
    def get_vertices_with_path(goal: Vertex) -> List[Vertex]:
        visited = [goal]
        vertices_queue = collections.deque(visited)
        while vertices_queue:
            vertex = vertices_queue.popleft()
            for parent in vertex.parents:
                # Todo: move to the foo
                if parent not in visited \
                        and parent.vertex_type == VERTEX_TYPE.INTERMEDIATE \
                        and not parent.code.is_full():
                    vertices_queue.append(parent)
                    visited.append(parent)
        # Remove goal
        return visited[1:]

    def create_vertex(self, code: Code, code_info: CodeInfo) -> Vertex:
        vertex = Vertex(self, code=code)
        vertex.add_code_info(code_info)
        if vertex.serialized_code.is_full():
            log.info(f'Connect full code to the end vertex')
            self.connect_to_end_vertex(vertex)
        self._dist.add_dist(vertex)
        return vertex

    def find_vertex(self, canon_tree: ast.AST) -> Optional[Vertex]:
        vertices = self.get_traversal()
        vertices.remove(self.start_vertex)
        for vertex in vertices:
            if are_asts_equal(vertex.serialized_code.canon_tree, canon_tree):
                log.info(f'Found an existing vertex for canon_tree: {str(get_code_from_tree(canon_tree))}')
                return vertex
        return None

    def find_or_create_vertex(self, code: Optional[Code], code_info: CodeInfo) -> Vertex:
        if code is None:
            log_and_raise_error('Code should not be None', log)
        vertex = self.find_vertex(code.canon_tree)
        if vertex:
            vertex.add_code_info(code_info)
            anon_tree_file = vertex.serialized_code.add_anon_tree(code.anon_tree)
            if anon_tree_file:
                self._dist.update_dist(vertex, anon_tree_file)
                vertex.add_anon_tree_nodes_number()
            return vertex
        log.info(f'Not found any existing vertex for code: {str(code)}, creating a new one')
        return self.create_vertex(code, code_info)

    def connect_to_start_vertex(self, vertex: Vertex) -> None:
        self._start_vertex.add_child(vertex)

    def connect_to_end_vertex(self, vertex: Vertex) -> None:
        self._end_vertex.add_parent(vertex)

    def add_code_info_chain(self, code_info_chain: Optional[List[Tuple[Code, CodeInfo]]]) -> None:
        log.info(f'Start adding code-info chain')
        if code_info_chain is None:
            log_and_raise_error(f'Code-info chain should not be None', log)
        if code_info_chain:
            log.info(f'Connect the first vertex in a chain to the start vertex')
            code, code_info = code_info_chain[0]
            first_vertex = self.find_or_create_vertex(code, code_info)
            self.connect_to_start_vertex(first_vertex)

            prev_vertex = first_vertex
            for next_code, next_code_info in code_info_chain[1:]:
                next_vertex = self.find_or_create_vertex(next_code, next_code_info)
                prev_vertex.add_child(next_vertex)
                prev_vertex = next_vertex
        log.info(f'Finish adding code-info chain')

    def get_dist_between_vertices(self, src_vertex: Vertex, dst_vertex: Vertex) -> int:
        return self._dist.get_dist(src_vertex, dst_vertex)

    def __str__(self) -> str:
        vertices_str = ''
        vertices = self.get_traversal()
        vertices_str += str(self.start_vertex) + '\n'
        vertices.remove(self.start_vertex)
        for vertex in vertices:
            vertices_str += str(vertex) + '\n'
        return f'Task: {self._task.value}\n' \
               f'Language: {self._language.value}\n' \
               f'Vertices:\n{vertices_str}\n'
