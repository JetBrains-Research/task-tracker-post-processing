# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import ast
import logging
from typing import Type
from abc import ABCMeta, abstractmethod

from src.main.util import consts
from src.main.solution_space.serialized_code import AnonTree
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.measured_vertex.measured_tree import IMeasuredTree

log = logging.getLogger(consts.LOGGER_NAME)


class IPathFinder(object, metaclass=ABCMeta):

    def __init__(self, graph: SolutionGraph, measured_vertex_subclass: Type[IMeasuredTree]):
        self._graph = graph
        self._measured_vertex_subclass = measured_vertex_subclass

    @property
    def graph(self) -> SolutionGraph:
        return self._graph

    @property
    def measured_vertex_subclass(self) -> Type[IMeasuredTree]:
        return self._measured_vertex_subclass

    def get_measured_tree(self, user_tree: AnonTree, candidate_tree: AnonTree) -> IMeasuredTree:
        return self._measured_vertex_subclass(user_tree, candidate_tree)

    # Find the next anon tree
    # Make sure code_info_list from user_anon_tree contains one code_info
    @abstractmethod
    def find_next_anon_tree(self, user_anon_tree: AnonTree, user_canon_tree: ast.AST) -> AnonTree:
        raise NotImplementedError
