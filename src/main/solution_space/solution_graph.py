# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
import ast
import os
import logging
import collections
from typing import Optional, List, Tuple, Set, Dict

from src.main.util.log_util import log_and_raise_error
from src.main.util.consts import LOGGER_NAME, TASK, LANGUAGE
from src.main.solution_space import consts as solution_space_consts
from src.main.canonicalization.diffs.diff_handler import IDiffHandler
from src.main.canonicalization.canonicalization import are_asts_equal
from src.main.solution_space.data_classes import User, Code, CodeInfo
from src.main.canonicalization.diffs.rivers_diff_handler import RiversDiffHandler
from src.main.util.file_util import remove_directory, create_directory, does_exist
from src.main.solution_space.consts import VERTEX_TYPE, GRAPH_FOLDER_PREFIX, FOLDER_WITH_CODE_FILES, FILE_PREFIX

log = logging.getLogger(LOGGER_NAME)


class Vertex:
    _last_id = 0

    def __init__(self, graph: 'SolutionGraph', code: Code = None,
                 vertex_type: solution_space_consts.VERTEX_TYPE = solution_space_consts.VERTEX_TYPE.INTERMEDIATE):
        self._parents = []
        self._children = []
        self._code_info_list = []
        self._code = code
        self._vertex_type = vertex_type

        self._id = self._last_id
        self.__class__._last_id += 1

        if code:
            if not does_exist(graph.graph_directory):
                msg = f'The graph with id {graph.id} does not have directory for vertex code. Expected graph ' \
                          f'folder prefix: {graph.graph_folder_prefix}{graph.id}'
                log_and_raise_error(msg, log, OSError)

            graph_folder_prefix = graph.graph_folder_prefix + str(graph.id) + '_' + graph.file_prefix
            code.create_file_with_code(graph.graph_directory, graph_folder_prefix, graph.language)

    @property
    def id(self) -> int:
        return self._id

    @property
    def parents(self) -> List['Vertex']:
        return self._parents

    @property
    def children(self) -> List['Vertex']:
        return self._children

    @property
    def code_info_list(self) -> List[CodeInfo]:
        return self._code_info_list

    @property
    def code(self) -> Code:
        return self._code

    @property
    def vertex_type(self) -> solution_space_consts.VERTEX_TYPE:
        return self._vertex_type

    # Use '' for better understanding.
    # See: https://stackoverflow.com/questions/15853469/putting-current-class-as-return-type-annotation
    def __add_parent_to_list(self, parent: 'Vertex') -> None:
        self._parents.append(parent)

    def __add_child_to_list(self, child: 'Vertex') -> None:
        self._children.append(child)

    def add_child(self, child: 'Vertex') -> None:
        self.__add_child_to_list(child)
        child.__add_parent_to_list(self)

    def add_parent(self, parent: 'Vertex') -> None:
        self.__add_parent_to_list(parent)
        parent.__add_child_to_list(self)

    def add_code_info(self, code_info: CodeInfo) -> None:
        self._code_info_list.append(code_info)

    def get_unique_users(self) -> Set[User]:
        users = [code_info.user for code_info in self._code_info_list]
        return set(users)

    def get_diffs_number_to_vertex(self, start_dh: IDiffHandler) -> int:
        return min(start_dh.get_diffs_number(a_t, self.code.canon_tree) for a_t in self.code.anon_trees)

    # Todo: change default handler and add type annotation to type_handler
    def get_diffs_number_from_vertex(self, end_dh: IDiffHandler,
                                     diff_handler_class: IDiffHandler = RiversDiffHandler) -> int:
        return min(diff_handler_class(anon_tree=a_t, canon_tree=self.code.canon_tree)
                   .get_diffs_number_from_diff_handler(end_dh) for a_t in self.code.anon_trees)


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


class SolutionGraph(collections.abc.Iterable):
    _last_id = 0
    folder_with_code_files = FOLDER_WITH_CODE_FILES

    def __init__(self, task: TASK, language: LANGUAGE = LANGUAGE.PYTHON, to_delete_old_graph: bool = True,
                 graph_folder_prefix: str = GRAPH_FOLDER_PREFIX, file_prefix: str = FILE_PREFIX):
        if language == LANGUAGE.NOT_DEFINED:
            log_and_raise_error(f'Error during constructing a solution graph. Language is not defined', log)
        self._task = task
        self._language = language

        self._id = self._last_id
        self.__class__._last_id += 1

        self._start_vertex = Vertex(self, vertex_type=solution_space_consts.VERTEX_TYPE.START)
        self._end_vertex = Vertex(self, vertex_type=solution_space_consts.VERTEX_TYPE.END)

        self._graph_folder_prefix = graph_folder_prefix
        self._file_prefix = file_prefix
        self._graph_directory = self.__get_graph_directory()

        if to_delete_old_graph:
            remove_directory(self._graph_directory)
        self.__create_graph_directory()

    @property
    def id(self) -> int:
        return self._id

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

    def __get_graph_directory(self) -> str:
        return os.path.join(self.__class__.folder_with_code_files, str(self._task.value),
                            self._graph_folder_prefix + str(self._id))

    def __create_graph_directory(self) -> None:
        create_directory(self._graph_directory)

    def __iter__(self) -> GraphIterator:
        return GraphIterator(self._start_vertex)

    def get_traversal(self) -> List[Vertex]:
        return self.__iter__().traversal

    # Todo: add tests
    @staticmethod
    def get_vertexes_with_path(goal: Vertex) -> List[Vertex]:
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
        if code.is_full():
            log.info(f'Connect full code to the end vertex')
            self.connect_to_end_vertex(vertex)
        return vertex

    def find_vertex(self, code: Code) -> Optional[Vertex]:
        vertices = self.get_traversal()
        vertices.remove(self.start_vertex)
        for vertex in vertices:
            if are_asts_equal(vertex.code.canon_tree, code.canon_tree):
                log.info(f'Found an existing vertex for code: {str(code)}')
                return vertex
        return None

    def find_vertex_by_canon_tree(self, canon_tree: ast.AST) -> Optional[Vertex]:
        return self.find_vertex(Code(canon_tree=canon_tree))

    def find_or_create_vertex(self, code: Optional[Code], code_info: CodeInfo) -> Vertex:
        if code is None:
            log_and_raise_error('Code should not be None', log)
        vertex = self.find_vertex(code)
        if vertex:
            vertex.add_code_info(code_info)
            return vertex
        log.info(f'Not found any existing vertex for code: {str(code)}, creating a new one')
        return self.create_vertex(code, code_info)

    def connect_to_start_vertex(self, vertex: Vertex) -> None:
        self._start_vertex.add_child(vertex)

    def connect_to_end_vertex(self, vertex: Vertex) -> None:
        self._end_vertex.add_parent(vertex)

    def add_code_info_chain(self, code_info_chain: Optional[List[Tuple[Code, CodeInfo]]]) -> None:
        log.info(f'Start adding code-user chain')
        if code_info_chain is None:
            log_and_raise_error(f'Code info chain should not be None', log)
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
        log.info(f'Finish adding code-user chain')

    def get_adj_list_with_ids(self) -> Dict[int, Set[int]]:
        adj_list = {}
        vertices = self.get_traversal()
        vertices.remove(self.start_vertex)
        for vertex in vertices:
            adj_vertices = adj_list.get(vertex.id, set())
            for c in vertex.children:
                adj_vertices.add(c.id)
            adj_list[vertex.id] = adj_vertices
        return adj_list

    # Todo: calculate diffs to the nearest goal from each vertex during graph constructing
    @staticmethod
    def get_diffs_number_between_vertexes(from_vertex: Vertex, to_vertex: Vertex,
                                          diff_handler_class: IDiffHandler = RiversDiffHandler) -> int:
        diffs = []
        for anon_tree in from_vertex.code.anon_trees:
            dh = diff_handler_class(anon_tree=anon_tree, canon_tree=from_vertex.code.canon_tree)
            diffs.append(to_vertex.get_diffs_number_to_vertex(dh))
        return min(diffs)
