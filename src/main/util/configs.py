# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
import collections
from enum import Enum
from typing import List


class ACTIONS_TYPE(Enum):
    PREPROCESSING = 'preprocessing'
    STATISTICS = 'statistics'
    ALGO = 'algo'
    TEST_SYSTEM = 'test_system'

    @classmethod
    def actions(cls) -> List['ACTIONS_TYPE']:
        return [_ for _ in ACTIONS_TYPE]

    @classmethod
    def values(cls) -> List[str]:
        return [a_t.value for a_t in ACTIONS_TYPE]


DEFAULT_LEVEL_VALUE = -1


class PREPROCESSING_LEVEL(Enum):
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
               f'{PREPROCESSING_LEVEL.MERGE.value} - merge activity-tracker and code-tracker files; ' \
               f'{PREPROCESSING_LEVEL.TESTS_RESULTS.value} - find tests results for the tasks; ' \
               f'{PREPROCESSING_LEVEL.SPLIT.value} - split data; ' \
               f'{PREPROCESSING_LEVEL.INTERMEDIATE_DIFFS.value} - remove intermediate diffs; ' \
               f'{PREPROCESSING_LEVEL.INEFFICIENT_STATEMENTS.value} - remove inefficient statements; ' \
               f'{PREPROCESSING_LEVEL.INT_EXPERIENCE.value} - add int experience column; '

    @classmethod
    def get_level(cls, level: str) -> 'PREPROCESSING_LEVEL':
        message = f'Preprosessing level has to be an integer number from {PREPROCESSING_LEVEL.min_value()} ' \
                  f'to {PREPROCESSING_LEVEL.max_value()}'
        try:
            level = int(level)
        except ValueError:
            raise ValueError(message)

        level = PREPROCESSING_LEVEL.max_value() if level == DEFAULT_LEVEL_VALUE else level
        if level < PREPROCESSING_LEVEL.min_value() or level > PREPROCESSING_LEVEL.max_value():
            raise ValueError(message)
        try:
            return PREPROCESSING_LEVEL(level)
        except ValueError:
            raise ValueError(message)


class ALGO_LEVEL(Enum):
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
        return f'{ALGO_LEVEL.CONSTRUCT.value} - construct a solution graph; ' \
               f'{ALGO_LEVEL.HINT.value} - run the main algo and get a hint, default value; '

    @classmethod
    def get_level(cls, level: str) -> 'ALGO_LEVEL':
        message = f'Algo level has to be an integer number from {ALGO_LEVEL.min_value()} ' \
                  f'to {ALGO_LEVEL.max_value()}'
        try:
            level = int(level)
        except ValueError:
            raise ValueError(message)

        level = ALGO_LEVEL.max_value() if level == DEFAULT_LEVEL_VALUE else level
        if level < ALGO_LEVEL.min_value() or level > ALGO_LEVEL.max_value():
            raise ValueError(message)
        try:
            return ALGO_LEVEL(level)
        except ValueError:
            raise ValueError(message)
