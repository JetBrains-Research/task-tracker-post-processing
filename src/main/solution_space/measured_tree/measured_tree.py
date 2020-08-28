# Copyright (c) by anonymous author(s)

from __future__ import annotations

from typing import Tuple
from abc import ABCMeta, abstractmethod

from src.main.util.consts import TASK
from src.main.solution_space.serialized_code import AnonTree
from src.main.canonicalization.diffs.gumtree import GumTreeDiff


class IMeasuredTree(object, metaclass=ABCMeta):

    def __init__(self, user_tree: AnonTree, candidate_tree: AnonTree, task: TASK):
        self._user_tree = user_tree
        self._candidate_tree = candidate_tree
        self.__init_diffs_number_and_rollback_probability()
        self._users_count = len(candidate_tree.get_unique_users())
        self._distance_to_user, self._distance_info = self.__calculate_distance_to_user()
        self._task = TASK

    @abstractmethod
    def __init_diffs_number_and_rollback_probability(self) -> None:
        self._diffs_number, delete_edits = GumTreeDiff \
            .get_diffs_and_delete_edits_numbers(self.user_tree.tree_file, self.candidate_tree.tree_file)
        self._rollback_probability = 0 if self._diffs_number == 0 else delete_edits / self._diffs_number

    @property
    def distance_to_user(self) -> float:
        return self._distance_to_user

    @property
    def distance_info(self) -> str:
        return self._distance_info

    @property
    def user_tree(self) -> AnonTree:
        return self._user_tree

    @property
    def candidate_tree(self) -> AnonTree:
        return self._candidate_tree

    @property
    def diffs_number(self) -> int:
        return self._diffs_number

    @property
    def rollback_probability(self) -> float:
        return self._rollback_probability

    @property
    def users_number(self) -> int:
        return self._users_count

    # Together with distance (float) we want to get distance info (str) to know how distance was count
    @abstractmethod
    def __calculate_distance_to_user(self) -> Tuple[float, str]:
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, o: object):
        raise NotImplementedError

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, IMeasuredTree):
            return False
        return not (self.__lt__(o) or o.__lt__(self))





