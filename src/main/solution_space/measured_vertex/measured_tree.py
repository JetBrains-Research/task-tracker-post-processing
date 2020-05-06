# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

from abc import ABCMeta, abstractmethod

from src.main.solution_space.serialized_code import AnonTree


class IMeasuredTree(object, metaclass=ABCMeta):

    def __init__(self, user_tree: AnonTree, candidate_tree: AnonTree):
        self._user_tree = user_tree
        self._candidate_tree = candidate_tree
        self._distance_to_user = 0
        self._users_count = 0
        # self._distance_to_user = distance_to_user if distance_to_user \
        #     else vertex.get_dist(user_vertex)
        # self._users_count = len(vertex.get_unique_users())

    @property
    def user_tree(self) -> AnonTree:
        return self._user_tree

    @property
    def candidate_tree(self) -> AnonTree:
        return self._candidate_tree

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
        if not isinstance(o, IMeasuredTree):
            return False
        return not (self.__lt__(o) or o.__lt__(self))

    def get_distance(self):
        pass




