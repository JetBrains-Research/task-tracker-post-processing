# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
import collections

from typing import Optional, List, Tuple, Set, Any

from src.main.gum_tree_diff.gum_tree_diff import get_diffs_number
from src.main.solution_space import consts as solution_space_consts
from src.main.canonicalization.canonicalization import are_asts_equal
from src.main.solution_space.data_classes import User, Code, CodeInfo
from src.main.util.consts import LOGGER_NAME, TASK, LANGUAGE, DEFAULT_VALUES
from src.main.util.file_util import remove_directory, create_directory, does_exist
from src.main.solution_space.consts import VERTEX_TYPE, GRAPH_FOLDER_PREFIX, FOLDER_WITH_CODE_FILES, FILE_PREFIX, \
    EMPTY_CODE_FILE

log = logging.getLogger(LOGGER_NAME)


class Vertex:
    def __init__(self, graph: 'SolutionGraph', code: Code = None,
                 vertex_type: solution_space_consts.VERTEX_TYPE = solution_space_consts.VERTEX_TYPE.INTERMEDIATE):
        self._parents = []
        self._children = []
        self._code_info_ist = []
        self._code = code
        self._vertex_type = vertex_type

        if code:
            if not does_exist(graph.graph_directory):
                log.error(f'The graph with id {graph.id} does not have directory for vertex code. Expected graph '
                          f'folder prefix: {graph.graph_folder_prefix}{graph.id}')
                raise OSError(f'The graph with id {graph.id} does not have directory for vertex code. Expected '
                              f'graph folder prefix: {graph.graph_folder_prefix}{graph.id}')

            graph_folder_prefix = graph.graph_folder_prefix + str(graph.id) + '_' + graph.file_prefix
            code.create_file_with_code(graph.graph_directory, graph_folder_prefix, graph.language)

    @property
    def parents(self) -> List['Vertex']:
        return self._parents

    @property
    def children(self) -> List['Vertex']:
        return self._children

    @property
    def code_info_list(self) -> List[CodeInfo]:
        return self._code_info_ist

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
        self._code_info_ist.append(code_info)

    def get_unique_users(self) -> Set[User]:
        users = [code_info.user for code_info in self._code_info_ist]
        return set(users)


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
            log.error(f'Error during constructing a solution graph. Language is not defined')
            raise ValueError(f'Error during constructing a solution graph. Language is not defined')
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
            if are_asts_equal(vertex.code.ast, code.ast):
                log.info(f'Found an existing vertex for code: {str(code)}')
                return vertex
        return None

    def find_or_create_vertex(self, code: Optional[Code], code_info: CodeInfo) -> Vertex:
        if code is None:
            log.error('Code should not be None')
            raise ValueError('Code should not be None')
        vertex = self.find_vertex(code)
        if vertex:
            vertex.add_code_info(code_info)
            return vertex
        log.info(f'Not found any existing vertex for code: {str(code)}, creating a new one')
        return self.create_vertex(code, code_info)

    def connect_to_start_vertex(self, vertex) -> None:
        self._start_vertex.add_child(vertex)

    def connect_to_end_vertex(self, vertex) -> None:
        self._end_vertex.add_parent(vertex)

    def add_code_info_chain(self, code_info_chain: Optional[List[Tuple[Code, CodeInfo]]]) -> None:
        log.info(f'Start adding code-user chain')
        if code_info_chain is None:
            log.error(f'Code info chain should not be None')
            raise ValueError(f'Code info chain should not be None')
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
