# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.solution_space import consts as solution_space_consts
from src.main.solution_space.data_classes import User, Code


class SolutionGraph:
    pass


class Vertex:
    def __init__(self, ast=None, vertex_type=solution_space_consts.VERTEX_TYPE.MIDDLE.value):
        self._parents = []
        self._children = []
        self._users = []
        self._ast = ast
        self._vertex_type = vertex_type

    @property
    def parents(self):
        return self._parents

    @property
    def children(self):
        return self._children

    @property
    def users(self):
        return self._users

    @property
    def ast(self):
        return self._ast

    @property
    def vertex_type(self):
        return self._vertex_type

    def add_parent_to_list(self, parent) -> None:
        self._parents.append(parent)
