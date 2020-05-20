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

