# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import ast
from typing import List, Set, Optional

import src.main.solution_space.solution_graph as sg
<<<<<<< HEAD
from src.main.solution_space.code_1 import Code, SerializedCode
=======
from src.main.util.helper_classes.id_counter import IdCounter
>>>>>>> solution-space/dev
from src.main.solution_space.data_classes import CodeInfo, User
from src.main.solution_space import consts as solution_space_consts
from src.main.util.helper_classes.pretty_string import PrettyString
from src.main.solution_space.serialized_code import Code, SerializedCode


class Vertex(IdCounter, PrettyString):

    def __init__(self, graph: sg.SolutionGraph, code: Optional[Code] = None,
                 vertex_type: solution_space_consts.VERTEX_TYPE = solution_space_consts.VERTEX_TYPE.INTERMEDIATE):
        super().__init__()
        self._parents = []
        self._children = []
        self._code_info_list = []
        self._graph = graph
        self._serialized_code = None if code is None \
            else SerializedCode.from_code(code, graph.graph_directory, graph.file_prefix)
        self._vertex_type = vertex_type

    @property
    def graph(self) -> sg.SolutionGraph:
        return self._graph

    @property
    def parents(self) -> List[Vertex]:
        return self._parents

    @property
    def children(self) -> List[Vertex]:
        return self._children

    @property
    def code_info_list(self) -> List[CodeInfo]:
        return self._code_info_list

    @property
    def canon_tree(self) -> ast.AST:
        return self._serialized_code.canon_tree

    @property
    def serialized_code(self) -> SerializedCode:
        return self._serialized_code

    @property
    def vertex_type(self) -> solution_space_consts.VERTEX_TYPE:
        return self._vertex_type

    def __add_parent_to_list(self, parent: Vertex) -> None:
        self._parents.append(parent)

    def __add_child_to_list(self, child: Vertex) -> None:
        self._children.append(child)

    def add_child(self, child: Vertex) -> None:
        self.__add_child_to_list(child)
        child.__add_parent_to_list(self)

    def add_parent(self, parent: Vertex) -> None:
        self.__add_parent_to_list(parent)
        parent.__add_child_to_list(self)

    def add_code_info(self, code_info: CodeInfo) -> None:
        self._code_info_list.append(code_info)

    def get_unique_users(self) -> Set[User]:
        users = [code_info.user for code_info in self._code_info_list]
        return set(users)

    def get_dist(self, dst_vertex: Vertex) -> int:
        return self._graph.get_dist_between_vertices(self, dst_vertex)

    def __str__(self) -> str:
        return f'Vertex id: {self._id}\n' \
               f'Vertex type: {self._vertex_type.value}\n' \
               f'Serialized_code: {self._serialized_code}\n' \
               f'Code info:\n{list(map(str, self._code_info_list))}\n' \
               f'Parents ids:\n{list(map(lambda parent: parent.id, self._parents))}\n' \
               f'Children:\n{list(map(lambda parent: parent.id, self._children))}'
