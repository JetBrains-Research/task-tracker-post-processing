# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import List
from src.main.solution_space.data_classes import User, Code
from src.main.solution_space import consts as solution_space_consts


class SolutionGraph:
    pass


class Vertex:
    def __init__(self, code=None, vertex_type=solution_space_consts.VERTEX_TYPE.MIDDLE.value):
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
