# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.data_classes import Profile, User
from src.main.solution_space.path_finder.path_finder import log
from src.main.solution_space.measured_vertex.measured_vertex import IMeasuredVertex


class MeasuredVertexV1(IMeasuredVertex):

    # Todo: get actual vertex profile
    @classmethod
    def _IMeasuredVertex__init_profile(self, user: User) -> Profile:
        return Profile()

    def __eq__(self, o: object) -> bool:
        """
        1. If o is not an instance of class, return False
        2. If any of distance_to_user or profile aren't equal, return False
        3. Otherwise, return True
        """
        if not isinstance(o, MeasuredVertexV1):
            return False
        if self._distance_to_user != o.distance_to_user or self._profile == o.profile:
            return False
        return True

    def __ne__(self, o: object) -> bool:
        """
        1. Return not __eq__
        """
        return not self.__eq__(o)

    def __lt__(self, o: object):
        """
        1. If o is not an instance of class, raise an error
        2. Compare distance
        3. Compare users_count
        """
        if not isinstance(o, MeasuredVertexV1):
            log_and_raise_error(f'The object {o} is not {self.__class__} class', log)
        if self._distance_to_user < o.distance_to_user:
            return True
        # Todo: use profile info
        return self._users_count < o.users_count
