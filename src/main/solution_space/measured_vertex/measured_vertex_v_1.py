# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
from __future__ import annotations

from typing import Optional

from src.main.solution_space.data_classes import Profile, User
from src.main.solution_space.measured_vertex.measured_vertex import IMeasuredVertex
from src.main.solution_space.path_finder.path_finder import log
from src.main.solution_space.vertex import Vertex
from src.main.util.log_util import log_and_raise_error


class MeasuredVertexV1(IMeasuredVertex):
    _description = \
        """
        version: 1
        *description*
        """

    def __init__(self, user_vertex: Vertex, vertex: Vertex, distance_to_user: Optional[int] = None):
        super().__init__(user_vertex, vertex, distance_to_user)

    @classmethod
    def description(cls) -> str:
        return cls._description

    # Todo: get actual vertex profile
    @classmethod
    def __init_profile(self, user: User) -> Profile:
        return Profile()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, MeasuredVertexV1):
            return False
        if self._distance_to_user != o.distance_to_user or self._profile == o.profile:
            return False
        return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __lt__(self, o: object):
        if not isinstance(o, MeasuredVertexV1):
            log_and_raise_error(f'The object {o} is not {self.__class__} class', log)
        if self._distance_to_user < o.distance_to_user:
            return True
        # Todo: use profile info
        return self._users_count < o.users_count
