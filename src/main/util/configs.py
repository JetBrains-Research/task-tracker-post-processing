# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from enum import Enum
from typing import List


class ACTIONS_TYPE(Enum):
    PREPROCESSING = 'preprocessing'
    STATISTICS = 'statistics'
    ALGO = 'algo'

    @classmethod
    def actions(cls) -> List['ACTIONS_TYPE']:
        return [_ for _ in ACTIONS_TYPE]

    @classmethod
    def values(cls) -> List[str]:
        return [a_t.value for a_t in ACTIONS_TYPE]


class PREPROCESSING_LEVEL(Enum):
    ALL = -1
    MERGE = 0
    TESTS_RESULTS = 1
    SPLIT = 2
    INTERMEDIATE_DIFFS = 3
    INEFFICIENT_STATEMENTS = 4
    INT_EXPERIENCE = 5

    @classmethod
    def min_value(cls) -> int:
        return min([a_t.value for a_t in PREPROCESSING_LEVEL])

    @classmethod
    def max_value(cls) -> int:
        return max([a_t.value for a_t in PREPROCESSING_LEVEL])

    @classmethod
    def description(cls) -> str:
        return f'the the Nth level runs all the level before it; ' \
               f'{PREPROCESSING_LEVEL.ALL.value} - use all preprocessing levels, default value; ' \
               f'{PREPROCESSING_LEVEL.MERGE.value} - merge activity-tracker and code-tracker files; ' \
               f'{PREPROCESSING_LEVEL.TESTS_RESULTS.value} - find tests results for the tasks; ' \
               f'{PREPROCESSING_LEVEL.SPLIT.value} - split data; ' \
               f'{PREPROCESSING_LEVEL.INTERMEDIATE_DIFFS.value} - remove intermediate diffs; ' \
               f'{PREPROCESSING_LEVEL.INEFFICIENT_STATEMENTS.value} - remove inefficient statements; ' \
               f'{PREPROCESSING_LEVEL.INT_EXPERIENCE.value} - add int experience column; '


class ALGO_LEVEL(Enum):
    TEST = -1
    CONSTRUCT = 0
    HINT = 1

    @classmethod
    def min_value(cls) -> int:
        return min([a_t.value for a_t in ALGO_LEVEL])

    @classmethod
    def max_value(cls) -> int:
        return max([a_t.value for a_t in ALGO_LEVEL])

    @classmethod
    def description(cls) -> str:
        return f'{ALGO_LEVEL.TEST.value} - run the path finder test system; ' \
               f'{ALGO_LEVEL.CONSTRUCT.value} - construct a solution graph; ' \
               f'{ALGO_LEVEL.HINT.value} - run the main algo and get a hint, default value; '
