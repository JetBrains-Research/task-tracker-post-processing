# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.path_finder.path_finder import log
from src.main.solution_space.measured_vertex.measured_tree import IMeasuredTree


class MeasuredTreeV1(IMeasuredTree):

    # Todo: use profile info for vertex and user_profile
    # Todo: 14/04 penalize for rollback
    def __lt__(self, o: object):
        """
        1. If o is not an instance of class, raise an error
        2. Compare distance
        3. Compare users_count
        """
        if not isinstance(o, MeasuredTreeV1):
            log_and_raise_error(f'The object {o} is not {self.__class__} class', log)
        if self._distance_to_user < o.distance_to_user:
            return True
        return self._users_count < o.users_count
