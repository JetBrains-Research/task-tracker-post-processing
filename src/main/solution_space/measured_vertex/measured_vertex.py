# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
from __future__ import annotations

from typing import Optional, Type, TypeVar
from abc import ABCMeta, abstractmethod

from src.main.solution_space.solution_graph import Vertex
from src.main.solution_space.data_classes import Profile, User

class IMeasuredVertex(object,  metaclass=ABCMeta):

    def __init__(self, user_vertex: Vertex, vertex: Vertex, distance_to_user: Optional[int] = None):
        # Todo: 14/04 add fine for rollback
        self._vertex = vertex
        self._distance_to_user = distance_to_user if distance_to_user \
            else vertex.get_dist(user_vertex)
        self._users_count = len(vertex.get_unique_users())
        self._profile = self.__init_profile(user_vertex.code_info_list[0].user)

    @classmethod
    @abstractmethod
    def get_description(cls) -> str:
        raise NotImplementedError

    # Todo: maybe not call here, but in user vertex?
    @abstractmethod
    def __init_profile(self, user: User) -> Profile:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, o: object) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __ne__(self, o: object) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, o: object):
        raise NotImplementedError

    @property
    def vertex(self) -> Vertex:
        return self._vertex

    @property
    def distance_to_user(self) -> int:
        return self._distance_to_user

    @property
    def profile(self) -> Profile:
        return self._profile

    @property
    def users_count(self) -> int:
        return self._users_count

