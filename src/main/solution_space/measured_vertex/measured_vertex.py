# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

from typing import Optional
from abc import ABCMeta, abstractmethod

from src.main.solution_space.solution_graph import Vertex
from src.main.solution_space.data_classes import Profile, User


class IMeasuredVertex(object,  metaclass=ABCMeta):

    def __init__(self, user_vertex: Vertex, vertex: Vertex, distance_to_user: Optional[int] = None):
        self._vertex = vertex
        self._distance_to_user = distance_to_user if distance_to_user \
            else vertex.get_dist(user_vertex)
        self._users_count = len(vertex.get_unique_users())

    @property
    def vertex(self) -> Vertex:
        return self._vertex

    @property
    def distance_to_user(self) -> int:
        return self._distance_to_user

    @property
    def users_count(self) -> int:
        return self._users_count

    @abstractmethod
    def __lt__(self, o: object):
        raise NotImplementedError

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, IMeasuredVertex):
            return False
        return not (self.__lt__(o) or o.__lt__(self))




