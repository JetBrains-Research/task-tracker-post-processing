# Copyright (c) by anonymous author(s)

import logging
from enum import Enum
from typing import Optional
from itertools import repeat

from src.main.util import consts
from src.main.util.log_util import log_and_raise_error

log = logging.getLogger(consts.LOGGER_NAME)


# Check if al least N (min_number_of_true) values are True
def contains_at_least_n_true(*values: bool, min_number_of_true: int = 2) -> bool:
    return sum(values) >= min_number_of_true


# Shows if the fragment is a solution problem or not
class HINT_SOLUTION(Enum):
    SOLUTION = 'solution'
    NOT_SOLUTION = 'not solution'

    @staticmethod
    def get_hint_solution(is_solution: bool, is_not_solution: bool) -> 'HINT_SOLUTION':
        if contains_at_least_n_true(is_solution, is_not_solution):
            log_and_raise_error(f'Incorrect value for the hint solution. At least two values are True', log)
        if is_solution:
            return HINT_SOLUTION.SOLUTION
        if is_not_solution:
            return HINT_SOLUTION.NOT_SOLUTION
        log_and_raise_error(f'Undefined hint solution value. Passed values:\nis_solution {is_solution}\n'
                            f'is_not_solution {is_not_solution}', log)


# Shows a hint size
# Note: is valid only for HINT_SOLUTION.NOT_SOLUTION otherwise is None
class HINT_SIZE(Enum):
    SMALL = 'small'
    BIG = 'big'

    @staticmethod
    def get_hint_size(is_small: bool, is_big: bool) -> Optional['HINT_SIZE']:
        if contains_at_least_n_true(is_small, is_big):
            log_and_raise_error(f'Incorrect value for the hint size. At least two values are True. Passed values:\n'
                                f'is_small {is_small}\nis_big {is_big}', log)
        if is_small:
            return HINT_SIZE.SMALL
        if is_big:
            return HINT_SIZE.BIG
        return None


# Shows a hint structure
# Note: is valid only for HINT_SOLUTION.SOLUTION otherwise is None
class HINT_STRUCTURE(Enum):
    SIMILAR = 'similar'
    DISSIMILAR = 'dissimilar'

    @staticmethod
    def get_hint_structure(is_similar: bool, is_dissimilar: bool) -> Optional['HINT_STRUCTURE']:
        if contains_at_least_n_true(is_similar, is_dissimilar):
            log_and_raise_error(f'Incorrect value for the hint structure. At least two values are True. '
                                f'Passed values:\nis_similar{is_similar}\nis_dissimilar {is_dissimilar}', log)
        if is_similar:
            return HINT_STRUCTURE.SIMILAR
        if is_dissimilar:
            return HINT_STRUCTURE.DISSIMILAR
        return None


# Shows a distance between hint and current solution structure
# Note: is valid only for HINT_SOLUTION.SOLUTION otherwise is None
class HINT_TO_SOLUTION_DISTANCE(Enum):
    CLOSE = 'close'
    SAME_TREE = 'same tree'
    FAR = 'far'
    UNCLEAR = 'unclear'

    @staticmethod
    def get_hint_to_solution_distance(is_approximate: bool, is_same_tree: bool, is_remote: bool,
                                      is_unclear: bool) -> Optional['HINT_TO_SOLUTION_DISTANCE']:
        if contains_at_least_n_true(is_approximate, is_same_tree, is_remote, is_unclear):
            log_and_raise_error(f'Incorrect value for the hint to solution distance. At least two values are True. '
                                f'Passed values:\nis_approximate {is_approximate}\nis_same_tree {is_same_tree}\n'
                                f'is_remote {is_remote}\nis_unclear {is_unclear}', log)
        if is_approximate:
            return HINT_TO_SOLUTION_DISTANCE.CLOSE
        if is_same_tree:
            return HINT_TO_SOLUTION_DISTANCE.SAME_TREE
        if is_remote:
            return HINT_TO_SOLUTION_DISTANCE.FAR
        if is_unclear:
            return HINT_TO_SOLUTION_DISTANCE.UNCLEAR
        return None


# Shows a hint step size
# Note: is valid only for HINT_SOLUTION.SOLUTION otherwise is None
class HINT_STEP(Enum):
    NORMAL = 'normal'
    BIG = 'big'
    SMALL = 'small'

    @staticmethod
    def get_hint_step(is_normal: bool, is_big: bool, is_small: bool) -> Optional['HINT_STEP']:
        if contains_at_least_n_true(is_normal, is_big, is_small):
            log_and_raise_error(f'Incorrect value for the hint step. At least two values are True. Passed values:\n'
                                f'is_normal {is_normal}\nis_big {is_big}\nis_small {is_small}', log)
        if is_normal:
            return HINT_STEP.NORMAL
        if is_big:
            return HINT_STEP.BIG
        if is_small:
            return HINT_STEP.SMALL
        return None


# Shows a hint quality
# Note: is valid only for HINT_SOLUTION.SOLUTION otherwise is None
class HINT_QUALITY(Enum):
    GOOD = 'good'
    NORMAL = 'normal'
    BAD = 'bad'

    @staticmethod
    def get_hint_quality(is_good: bool, is_normal: bool, is_bad: bool) -> Optional['HINT_QUALITY']:
        if contains_at_least_n_true(is_good, is_normal, is_bad):
            log_and_raise_error(f'Incorrect value for the hint quality. At least two values are True. Passed values:\n'
                                f'is_good {is_good}\nis_normal {is_normal}\nis_bad {is_bad}', log)
        if is_good:
            return HINT_QUALITY.GOOD
        if is_normal:
            return HINT_QUALITY.NORMAL
        if is_bad:
            return HINT_QUALITY.BAD
        return None


# Shows a code quality after diffs applied
# Note: is valid only for HINT_SOLUTION.SOLUTION otherwise is None
class QUALITY_AFTER_DIFFS_APPLIED(Enum):
    CORRECT = 'correct'
    INCORRECT = 'incorrect'

    @staticmethod
    def get_apply_diffs_quality(is_correct: bool, is_incorrect: bool) -> Optional['QUALITY_AFTER_DIFFS_APPLIED']:
        if contains_at_least_n_true(is_correct, is_incorrect):
            log_and_raise_error(f'Incorrect value for the apply diffs quality. At least two values are True. '
                                f'Passed values:\nis_correct {is_correct}\nis_incorrect {is_incorrect}', log)
        if is_correct:
            return QUALITY_AFTER_DIFFS_APPLIED.CORRECT
        if is_incorrect:
            return QUALITY_AFTER_DIFFS_APPLIED.INCORRECT
        return None
