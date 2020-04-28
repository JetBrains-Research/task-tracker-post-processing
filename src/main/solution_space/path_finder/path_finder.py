# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod

from src.main.canonicalization.canonicalization import get_trees, Optional, Type, TypeVar
from src.main.canonicalization.consts import TREE_TYPE
from src.main.solution_space.code_1 import Code
from src.main.solution_space.measured_vertex.measured_vertex import IMeasuredVertex
from src.main.util import consts
from src.main.solution_space.data_classes import User
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.util.consts import TEST_RESULT

log = logging.getLogger(consts.LOGGER_NAME)


class IPathFinder(object, metaclass=ABCMeta):

    # todo: add type
    def __init__(self, graph: SolutionGraph, measured_vertex: Type[IMeasuredVertex]):
        self._graph = graph
        self._measured_vertex = measured_vertex
        empty_anon, empty_canon = get_trees("", {TREE_TYPE.ANON, TREE_TYPE.CANON})
        # Todo: create empty vertex in a graph to not recount dist between empty and goal?
        self._empty_vertex = Vertex(graph, Code(empty_anon, empty_canon, TEST_RESULT.CORRECT_CODE.value))

    @property
    def graph(self) -> SolutionGraph:
        return self._graph

    def measured_vertex(self, user_vertex: Vertex, vertex: Vertex,
                        distance_to_user: Optional[int] = None) -> IMeasuredVertex:
        return self._measured_vertex(user_vertex, vertex, distance_to_user)

    @classmethod
    @abstractmethod
    def get_description(cls) -> str:
        raise NotImplementedError

    # Find a next canonicalized code state
    # Make sure that code_info_list has 1 element with code_info
    @abstractmethod
    def find_next_vertex(self, user_vertex: Vertex) -> Vertex:
        raise NotImplementedError
