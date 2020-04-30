# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import Type, Optional

from src.main.util import consts
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.solution_space.measured_vertex.measured_vertex import IMeasuredVertex

log = logging.getLogger(consts.LOGGER_NAME)


class IPathFinder(object, metaclass=ABCMeta):

    def __init__(self, graph: SolutionGraph, measured_vertex_subclass: Type[IMeasuredVertex]):
        self._graph = graph
        self._measured_vertex_subclass = measured_vertex_subclass

    @property
    def graph(self) -> SolutionGraph:
        return self._graph

    @property
    def measured_vertex_subclass(self) -> Type[IMeasuredVertex]:
        return self._measured_vertex_subclass

    def get_measured_vertex(self, user_vertex: Vertex, vertex: Vertex,
                            distance_to_user: Optional[int] = None) -> IMeasuredVertex:
        return self._measured_vertex_subclass(user_vertex, vertex, distance_to_user)

    # Find the next canonicalized code state
    # Make sure code_info_list of user_vertex has 1 element with code_info
    @abstractmethod
    def find_next_vertex(self, user_vertex: Vertex) -> Vertex:
        raise NotImplementedError
