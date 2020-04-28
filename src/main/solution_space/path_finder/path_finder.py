# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from abc import ABCMeta, abstractmethod

from src.main.util import consts
from src.main.solution_space.data_classes import User
from src.main.canonicalization.diffs.diff_handler import IDiffHandler
from src.main.solution_space.solution_graph import SolutionGraph, Vertex

log = logging.getLogger(consts.LOGGER_NAME)


class IPathFinder(object, metaclass=ABCMeta):
    def __init__(self, graph: SolutionGraph):
        self._graph = graph

    @property
    def graph(self) -> SolutionGraph:
        return self._graph

    @classmethod
    @abstractmethod
    def get_description(cls) -> str:
        raise NotImplementedError

    # Find a next canonicalized code state
    @abstractmethod
    def find_next_vertex(self, user_diff_handler: IDiffHandler, user: User) -> Vertex:
        raise NotImplementedError
