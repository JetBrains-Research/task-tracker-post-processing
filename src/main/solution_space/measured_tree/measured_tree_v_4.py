# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

from typing import Tuple

from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.consts import USERS_NUMBER
from src.main.solution_space.serialized_code import AnonTree
from src.main.solution_space.path_finder.path_finder import log
from src.main.solution_space.path_finder_test_system import doc_param, skip
from src.main.solution_space.measured_tree.measured_tree import IMeasuredTree

@skip('Version 7 is better')
class MeasuredTreeV4(IMeasuredTree):
    _age_w = 0.15
    _exp_w = 0.15
    _diffs_w = 0.6
    _users_w = -0.2
    _rollback_w = 2.0
    _rate_w = -0.3

    @doc_param(_diffs_w, _users_w, _rate_w, _rollback_w, _age_w, _exp_w)
    def _IMeasuredTree__calculate_distance_to_user(self) -> Tuple[float, str]:
        """
        Finds distance as weighted sum of:
        1. diffs_number, weight: {0}
        2. users_count, weight: {1}
        3. rate reducing, weight: {2}
        4. rollback probability, weight: {3}
        5. (if possible) abs difference between age, weight: {4}
        6. (if possible) abs difference between exp, weight: {5}
        """
        distance = self._diffs_w * self._diffs_number \
                   + self._users_w * self.users_number / USERS_NUMBER[self._task] \
                   + self._rate_w * (self.user_tree.rate - self.candidate_tree.rate) \
                   + self._rollback_w * self.rollback_probability
        distance_info = f'(diffs: {self._diffs_w} * {self._diffs_number}) + ' \
                        f'(users: {self._users_w} * {self.users_number} / {USERS_NUMBER[self._task]}) + ' \
                        f'(rate: {self._rate_w} * ({self.user_tree.rate} - {self.candidate_tree.rate})) + ' \
                        f'(rollback: {self._rollback_w} * {self.rollback_probability})'

        trees = [self.user_tree, self.candidate_tree]
        if AnonTree.have_non_empty_attr('_age_median', trees):
            distance += self._age_w * abs(self.user_tree.age_median - self.candidate_tree.age_median)
            distance_info += f' + (age: {self._age_w} * |{self.user_tree.age_median} - {self.candidate_tree.age_median}|)'
        if AnonTree.have_non_empty_attr('_experience_median', trees):
            distance += self._exp_w * abs(self.user_tree.experience_median - self.candidate_tree.experience_median)
            distance_info += f' + (exp: {self._exp_w} * |{self.user_tree.experience_median} - {self.candidate_tree.experience_median}|)'

        return (distance, distance_info)

    def __lt__(self, o: object):
        """
        1. If o is not an instance of class, raise an error
        2. Compare distance
        """
        if not isinstance(o, MeasuredTreeV4):
            log_and_raise_error(f'The object {o} is not {self.__class__} class', log)
        return self._distance_to_user < o._distance_to_user
