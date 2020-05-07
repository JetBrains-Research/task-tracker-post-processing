# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

from src.main.solution_space.consts import EMPTY_MEDIAN
from src.main.solution_space.path_finder_test_system import doc_param
from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.path_finder.path_finder import log
from src.main.solution_space.measured_tree.measured_tree import IMeasuredTree


class MeasuredTreeV1(IMeasuredTree):
    _age_w = 0.5
    _exp_w = 0.5
    _diffs_w = 7
    _users_w = 1
    _rollback_w = 1
    _rate_w = 1

    @doc_param(_diffs_w, _users_w, _rate_w, _rollback_w, _age_w, _exp_w)
    def _IMeasuredTree__calculate_distance_to_user(self) -> float:
        """
        Finds distance as weighted sum of:
        1. diffs_number, weight: {0}
        2. users_count, weight: {1}
        3. rate reducing, weight: {2}
        4. rollback probability, weight: {3}
        5. (if possible) abs difference between age, weight: {4}
        6. (if possible) abs difference between exp, weight: {5}
        """

        distance = self._diffs_w * self._diffs_number\
                   - self._users_w * self.users_count\
                   + self._rate_w * (self.user_tree.rate - self.candidate_tree.rate)\
                   + self._rollback_w * self.rollback_probability

        if not (self.user_tree.has_empty_age() or self.candidate_tree.has_empty_age()):
            distance += self._age_w * abs(self.user_tree.age_median - self.candidate_tree.age_median)
        if not (self.user_tree.has_empty_experience() or self.candidate_tree.has_empty_experience()):
            distance += self._exp_w * abs(self.user_tree.experience_median - self.candidate_tree.experience_median)
        return distance

    # Todo: use profile info for vertex and user_profile
    # Todo: 14/04 penalize for rollback
    def __lt__(self, o: object):
        """
        1. If o is not an instance of class, raise an error
        2. Compare distance
        """
        if not isinstance(o, MeasuredTreeV1):
            log_and_raise_error(f'The object {o} is not {self.__class__} class', log)
        return self._distance_to_user < o._distance_to_user

