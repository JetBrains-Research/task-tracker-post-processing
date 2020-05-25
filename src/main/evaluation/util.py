# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from enum import Enum
from typing import Optional

from src.main.util import consts
from src.main.util.log_util import log_and_raise_error

log = logging.getLogger(consts.LOGGER_NAME)


#Todo: fix names int the file and add tests

def at_least_two(*values) -> bool:
    if len(values) <= 1:
        return False
    res = values[0]
    for value in values[1:]:
        res = res and value
        if res:
            return True
        res = res or value
    return False


class HINT_SOLUTION(Enum):
    SOLUTION = 'solution'
    NOT_SOLUTION = 'not solution'

    @staticmethod
    def get_hint_solution(is_solution: bool, is_not_solution: bool) -> 'HINT_SOLUTION':
        if at_least_two(is_solution, is_not_solution):
            log_and_raise_error(f'Incorrect value for the hint solution. At least two values are True', log)
        if is_solution:
            return HINT_SOLUTION.SOLUTION
        if is_not_solution:
            return HINT_SOLUTION.NOT_SOLUTION
        log_and_raise_error(f'Undefined hint solution value', log)


class HINT_SIZE(Enum):
    SMALL = 'small'
    BIG = 'big'

    @staticmethod
    def get_hint_size(is_small: bool, is_big: bool) -> Optional['HINT_SIZE']:
        if at_least_two(is_small, is_big):
            log_and_raise_error(f'Incorrect value for the hint size. At least two values are True', log)
        if is_small:
            return HINT_SIZE.SMALL
        if is_big:
            return HINT_SIZE.BIG
        return None


class HINT_STRUCTURE(Enum):
    SIMILAR = 'similar'
    DISSIMILAR = 'disimilar'

    @staticmethod
    def get_hint_structure(is_similar: bool, is_dissimilar: bool) -> Optional['HINT_STRUCTURE']:
        if at_least_two(is_similar, is_dissimilar):
            log_and_raise_error(f'Incorrect value for the hint structure. At least two values are True', log)
        if is_similar:
            return HINT_STRUCTURE.SIMILAR
        if is_dissimilar:
            return HINT_STRUCTURE.DISSIMILAR
        return None


class HINT_TO_SOLUTION_DISTANCE(Enum):
    APPROXIMATE = 'approximate'
    SAME_TREE = 'same tree'
    REMOTE = 'remote'
    UNCLEAR = 'unclear'

    @staticmethod
    def get_hint_to_solution_distance(is_approximate: bool, is_same_tree: bool, is_remote: bool,
                                      is_unclear: bool) -> Optional['HINT_TO_SOLUTION_DISTANCE']:
        if at_least_two(is_approximate, is_same_tree, is_remote, is_unclear):
            log_and_raise_error(f'Incorrect value for the hint to solution distance. At least two values are True', log)
        if is_approximate:
            return HINT_TO_SOLUTION_DISTANCE.APPROXIMATE
        if is_same_tree:
            return HINT_TO_SOLUTION_DISTANCE.SAME_TREE
        if is_remote:
            return HINT_TO_SOLUTION_DISTANCE.REMOTE
        if is_unclear:
            return HINT_TO_SOLUTION_DISTANCE.UNCLEAR
        return None


class HINT_STEP(Enum):
    NORMAL = 'normal'
    BIG = 'big'
    SMALL = 'small'

    @staticmethod
    def get_hint_step(is_normal: bool, is_big: bool, is_small: bool) -> Optional['HINT_STEP']:
        if at_least_two(is_normal, is_big, is_small):
            log_and_raise_error(f'Incorrect value for the hint step. At least two values are True', log)
        if is_normal:
            return HINT_STEP.NORMAL
        if is_big:
            return HINT_STEP.BIG
        if is_small:
            return HINT_STEP.SMALL
        return None


class HINT_QUALITY(Enum):
    GOOD = 'good'
    NORMAL = 'normal'
    BAD = 'bad'

    @staticmethod
    def get_hint_quality(is_good: bool, is_normal: bool, is_bad: bool) -> Optional['HINT_QUALITY']:
        if at_least_two(is_good, is_normal, is_bad):
            log_and_raise_error(f'Incorrect value for the hint quality. At least two values are True', log)
        if is_good:
            return HINT_QUALITY.GOOD
        if is_normal:
            return HINT_QUALITY.NORMAL
        if is_bad:
            return HINT_QUALITY.BAD
        return None


class APPLY_DIFFS_QUALITY(Enum):
    CORRECT = 'correct'
    INCORRECT = 'incorrect'

    @staticmethod
    def get_apply_diffs_quality(is_correct: bool, is_incorrect: bool) -> Optional['APPLY_DIFFS_QUALITY']:
        if at_least_two(is_correct, is_incorrect):
            log_and_raise_error(f'Incorrect value for the apply diffs quality. At least two values are True', log)
        if is_correct:
            return APPLY_DIFFS_QUALITY.CORRECT
        if is_incorrect:
            return APPLY_DIFFS_QUALITY.INCORRECT
        return None

