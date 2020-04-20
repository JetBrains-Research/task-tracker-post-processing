# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
from __future__ import annotations

from typing import List, Set, Optional

import src.main.solution_space.solution_graph as sg
from src.main.solution_space.code import Code, SerializedCode
from src.main.solution_space.data_classes import CodeInfo, User
from src.main.solution_space import consts as solution_space_consts


class Vertex:
    _last_id = 0

    def __init__(self, graph: sg.SolutionGraph, code: Optional[Code] = None,
                 vertex_type: solution_space_consts.VERTEX_TYPE = solution_space_consts.VERTEX_TYPE.INTERMEDIATE):
        self._parents = []
        self._children = []
        self._code_info_list = []
        self._graph = graph
        self._serialized_code = None if code is None else SerializedCode.from_code(code, graph.graph_directory, graph.file_prefix)
        self._vertex_type = vertex_type

        self._id = self._last_id
        self.__class__._last_id += 1

    @property
    def id(self) -> int:
        return self._id

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
    def serialized_code(self) -> SerializedCode:
        return self._serialized_code

    @property
    def vertex_type(self) -> solution_space_consts.VERTEX_TYPE:
        return self._vertex_type

    # Use  for better understanding.
    # See: https://stackoverflow.com/questions/15853469/putting-current-class-as-return-type-annotation
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
