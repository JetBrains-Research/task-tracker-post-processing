# Copyright (c) by anonymous author(s)

import os
import ast
import logging
import collections
from collections import defaultdict
from typing import Optional, List, Tuple

from src.main.solution_space.vertex import Vertex
from src.main.util.math_util import get_safety_median
from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.serialized_code import Code
from src.main.solution_space.data_classes import CodeInfo
from src.main.util.default_dict_util import get_empty_list
from src.main.util.helper_classes.id_counter import IdCounter
from src.main.solution_space.distance import VertexDistanceMatrix
from src.main.util.helper_classes.pretty_string import PrettyString
from src.main.solution_space import consts as solution_space_consts
from src.main.util.file_util import remove_directory, create_directory
from src.main.util.consts import LOGGER_NAME, TASK, LANGUAGE, TEST_RESULT
from src.main.canonicalization.canonicalization import are_asts_equal, get_code_from_tree, AstStructure
from src.main.solution_space.consts import GRAPH_FOLDER_PREFIX, SOLUTION_SPACE_FOLDER, FILE_PREFIX, EMPTY_MEDIAN

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
                if child not in visited:
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
                 graph_folder_prefix: str = GRAPH_FOLDER_PREFIX, file_prefix: str = FILE_PREFIX):
        super().__init__()
        if language == LANGUAGE.UNDEFINED:
            log_and_raise_error(f'Error during constructing a solution graph. Language is not defined', log)
        self._task = task
        self._language = language

        self._graph_folder_prefix = graph_folder_prefix
        self._file_prefix = file_prefix
        self._graph_directory = self.get_default_graph_directory()

        self.canon_nodes_number_dict = defaultdict(get_empty_list)
        self.anon_nodes_number_dict = defaultdict(get_empty_list)
        self.goals_nodes_number_dict = defaultdict(get_empty_list)
        self.anon_structure_dict = defaultdict(get_empty_list)

        self._goals_median = None

        if to_delete_old_graph:
            remove_directory(self._graph_directory)
        create_directory(self._graph_directory)

        self._start_vertex = Vertex(self, vertex_type=solution_space_consts.VERTEX_TYPE.START)
        self._end_vertex = Vertex(self, vertex_type=solution_space_consts.VERTEX_TYPE.END)
        self._empty_vertex = Vertex(self, Code.from_source('', TEST_RESULT.CORRECT_CODE.value, language=language))
        self.connect_to_start_vertex(self._empty_vertex)

        self.dist = VertexDistanceMatrix(to_store_dist=False)

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

    @property
    def empty_vertex(self) -> Vertex:
        return self._empty_vertex

    # Todo: make something with all these median methods (and with same methods in AnonTree)
    @property
    def goals_median(self) -> int:
        return self._goals_median

    @goals_median.getter
    def goals_median(self) -> int:
        if self._goals_median is None:
            log_and_raise_error('Goal median is not found yet, you should call find_goals_median first', log)
        return self._goals_median

    def find_goals_median(self) -> None:
        goals_nodes_number = sum([[k] * len(v) for k, v in self.goals_nodes_number_dict.items()], [])
        self._goals_median = get_safety_median(goals_nodes_number, EMPTY_MEDIAN)

    def is_goals_median_empty(self) -> bool:
        if self._goals_median is None:
            log_and_raise_error('Goal median is not found yet, you should call find_goal_median first', log)
        return self._goals_median == EMPTY_MEDIAN

    def __iter__(self) -> GraphIterator:
        return GraphIterator(self._start_vertex)

    def is_empty_vertex(self, vertex: Vertex) -> bool:
        return vertex == self._empty_vertex

    def get_traversal(self, to_remove_start: bool = True, to_remove_end: bool = True) -> List[Vertex]:
        traversal = self.__iter__().traversal
        # Traversal always contains START_VERTEX, because it's a root for GraphIterator
        if to_remove_start:
            traversal.remove(self._start_vertex)
        # However, it may not contain END_VERTEX if there is no path from the root to it:
        if to_remove_end and self._end_vertex in traversal:
            traversal.remove(self._end_vertex)
        return traversal

    def get_default_graph_directory(self) -> str:
        return os.path.join(self.__class__.solution_space_folder, str(self._task.value),
                            f'{self._graph_folder_prefix}_{str(self._id)}')

    def recreate_graph_files(self, new_path_for_graph: Optional[str]) -> None:
        if new_path_for_graph is None:
            new_path_for_graph = self.get_default_graph_directory()
        self._graph_directory = new_path_for_graph

        for vertex in self.get_traversal():
            vertex.serialized_code.recreate_files_for_trees(self._graph_directory)

    def create_vertex(self, code: Code, code_info: CodeInfo) -> Vertex:
        vertex = Vertex(self, code=code, code_info=code_info)
        if vertex.serialized_code.is_full():
            log.info(f'Connect full code to the end vertex')
            self.connect_to_end_vertex(vertex)
            self.goals_nodes_number_dict[AstStructure.get_nodes_number_in_ast(vertex.serialized_code.canon_tree)].append(vertex.id)
        return vertex

    def find_vertex(self, canon_tree: ast.AST) -> Optional[Vertex]:
        for vertex in self.get_traversal():
            if are_asts_equal(vertex.canon_tree, canon_tree):
                log.info(f'Found an existing vertex {vertex.id} for canon_tree: {str(get_code_from_tree(canon_tree))}')
                return vertex
        return None

    def find_or_create_vertex(self, code: Optional[Code], code_info: CodeInfo) -> Vertex:
        if code is None:
            log_and_raise_error('Code should not be None', log)
        vertex = self.find_vertex(code.canon_tree)
        if vertex:
            anon_tree_file = vertex.serialized_code.add_anon_tree(code.anon_tree, code.rate, code_info)
            if anon_tree_file:
                vertex.add_anon_nodes_number_and_structure()
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
            first_code, first_code_info = code_info_chain[0]
            first_vertex = self.find_or_create_vertex(first_code, first_code_info)
            self.connect_to_start_vertex(first_vertex)

            prev_vertex = first_vertex
            prev_anon_tree = prev_vertex.serialized_code.find_anon_tree(first_code.anon_tree)
            for next_code, next_code_info in code_info_chain[1:]:
                next_vertex = self.find_or_create_vertex(next_code, next_code_info)
                prev_vertex.add_child(next_vertex)

                next_anon_tree = next_vertex.serialized_code.find_anon_tree(next_code.anon_tree)
                prev_anon_tree.add_next_anon_tree(next_anon_tree)

                prev_vertex = next_vertex
                prev_anon_tree = next_anon_tree
        log.info(f'Finish adding code-info chain')

    def find_all_medians(self) -> None:
        self.find_goals_median()
        for vertex in self.get_traversal():
            for anon_tree in vertex.serialized_code.anon_trees:
                anon_tree.find_medians()

    def __str__(self) -> str:
        vertices_str = ''
        vertices_str += f'Start vertex:\n{str(self.start_vertex)}\n'
        for vertex in self.get_traversal():
            vertices_str += str(vertex) + '\n'
        vertices_str += f'End vertex:\n{str(self.start_vertex)}\n'
        return f'Task: {self._task.value}\n' \
               f'Language: {self._language.value}\n' \
               f'Vertices:\n{vertices_str}\n'
