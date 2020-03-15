# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import collections
import logging
import queue
from typing import Optional, List, Tuple

from src.main.canonicalization.ast_tools import compareASTs
from src.main.solution_space import consts as solution_space_consts
from src.main.solution_space.consts import VERTEX_TYPE
from src.main.solution_space.data_classes import User, Code
from src.main.util.consts import LOGGER_NAME


log = logging.getLogger(LOGGER_NAME)


class Vertex:
    def __init__(self, code: Code = None, vertex_type=solution_space_consts.VERTEX_TYPE.INTERMEDIATE.value):
        self._parents = []
        self._children = []
        self._users = []
        self._code = code
        self._vertex_type = vertex_type

    @property
    def parents(self) -> List['Vertex']:
        return self._parents

    @property
    def children(self) -> List['Vertex']:
        return self._children

    @property
    def users(self) -> List[User]:
        return self._users

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

    def add_user(self, user: User) -> None:
        self._users.append(user)


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
                if child not in visited and child.vertex_type != VERTEX_TYPE.END.value:
                    vertices_queue.append(child)
                    visited.append(child)
        return visited

    def __next__(self):
        if self._cursor + 1 >= len(self._traversal):
            raise StopIteration
        self._cursor += 1
        return self._traversal[self._cursor]


class SolutionGraph(collections.abc.Iterable):
    def __init__(self):
        self._start_vertex = Vertex(vertex_type=solution_space_consts.VERTEX_TYPE.START.value)
        self._end_vertex = Vertex(vertex_type=solution_space_consts.VERTEX_TYPE.END.value)

    @property
    def start_vertex(self) -> Vertex:
        return self._start_vertex

    @property
    def end_vertex(self) -> Vertex:
        return self._end_vertex

    def __iter__(self) -> GraphIterator:
        return GraphIterator(self._start_vertex)

    def get_traversal(self):
        return self.__iter__().traversal

    def find_or_create_vertex(self, code: Optional[Code], user: User) -> Vertex:
        if code is None:
            log.info('Code should not be None')
            raise ValueError('Code should not be None')
        vertices = iter(self)
        for vertex in vertices:
            # todo: add tests for comparator
            # if compareAST == 0, then they are equal, so we should add 'not'
            if vertex.code and not compareASTs(vertex.code.ast, code.ast):
                log.info(f'Found an existing vertex for code: {str(code)}')
                vertex.add_user(user)
                return vertex
        log.info(f'Not found any existing vertex for code: {str(code)}, creating a new one')
        vertex = Vertex(code)
        vertex.add_user(user)
        if code.is_full():
            log.info(f'Connect full code to the end vertex')
            self.connect_to_end_vertex(vertex)
        return vertex

    def connect_to_start_vertex(self, vertex) -> None:
        self._start_vertex.add_child(vertex)

    def connect_to_end_vertex(self, vertex) -> None:
        self._end_vertex.add_parent(vertex)

    def add_code_user_chain(self, code_user_chain: List[Tuple[Code, User]]) -> None:
        log.info(f'Start adding code-user chain')
        if code_user_chain:
            log.info(f'Connect the first vertex in a chain to the start vertex')
            first_code_user = code_user_chain[0]
            first_vertex = self.find_or_create_vertex(first_code_user[0], first_code_user[1])
            self.connect_to_start_vertex(first_vertex)

            prev_vertex = first_vertex
            for next_code_user in code_user_chain[1:]:
                next_vertex = self.find_or_create_vertex(next_code_user[0], next_code_user[1])
                prev_vertex.add_child(next_vertex)
                prev_vertex = next_vertex
        log.info(f'Finish adding code-user chain')
