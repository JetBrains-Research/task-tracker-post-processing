# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from abc import ABCMeta, abstractmethod
from typing import Optional

from src.main.canonicalization.diffs.diff_handler import IDiffHandler
from src.main.util import consts
from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.data_classes import User, Profile
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.vertex import Vertex

log = logging.getLogger(consts.LOGGER_NAME)


class IPathFinder(object, metaclass=ABCMeta):
    def __init__(self, graph: SolutionGraph):
        self._graph = graph

    @property
    def graph(self) -> SolutionGraph:
        return self._graph

    # Find a next canonicalized code state
    @abstractmethod
    def find_next_vertex(self, user_diff_handler: IDiffHandler, user: User) -> Vertex:
        raise NotImplementedError


# Todo: move somewhere?
class MeasuredVertex:
    def __init__(self, user_diff_handler: IDiffHandler, vertex: Vertex, user: User, distance: Optional[int] = None):
        self._vertex = vertex
        self._distance = distance if distance else vertex.get_diffs_number_to_vertex(user_diff_handler)
        # Todo: get actual vertex profile
        self._profile = self.__init_profile(user)
        self._users_count = len(vertex.get_unique_users())

    @property
    def vertex(self) -> Vertex:
        return self._vertex

    @property
    def distance(self) -> int:
        return self._distance

    @property
    def profile(self) -> Profile:
        return self._profile

    @property
    def users_count(self) -> int:
        return self._users_count

    def __init_profile(self, user: User) -> Profile:
        # Todo: add user handling
        return Profile()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, MeasuredVertex):
            return False
        if self._distance != o.distance or self._profile == o.profile:
            return False
        return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __lt__(self, o: object):
        if not isinstance(o, MeasuredVertex):
            log_and_raise_error(f'The object {o} is not {self.__class__} class', log)
        if self._distance < o.distance:
            return True
        # Todo: use profile info
        return self._users_count < o.users_count



