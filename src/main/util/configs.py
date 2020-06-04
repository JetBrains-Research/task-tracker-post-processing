# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from enum import Enum
from typing import List


class PLOT_TYPE(Enum):
    PARTICIPANTS_DISTRIBUTION = 'participants_distr'
    TASKS_DISTRIBUTION = 'tasks_distr'
    SPLITTING_PLOTS = 'splitting_plots'

    @classmethod
    def plot_types(cls) -> List['PLOT_TYPE']:
        return [_ for _ in PLOT_TYPE]

    @classmethod
    def values(cls) -> List[str]:
        return [p_t.value for p_t in PLOT_TYPE]

    @classmethod
    def description(cls) -> str:
        return f'{PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value} - visualize participants distribution; ' \
               f'{PLOT_TYPE.TASKS_DISTRIBUTION.value} - visualize tasks distribution; ' \
               f'{PLOT_TYPE.SPLITTING_PLOTS.value} - visualize splitting plots;'

    @classmethod
    def str_to_plot_type(cls, value: str) -> 'PLOT_TYPE':
        try:
            return PLOT_TYPE(value.lower())
        except ValueError:
            raise ValueError(f'{value} is not a plot_type value. Available values: {PLOT_TYPE.description()}')


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

        if level < ALGO_LEVEL.min_value() or level > ALGO_LEVEL.max_value():
            raise ValueError(message)
        try:
            return ALGO_LEVEL(level)
        except ValueError:
            raise ValueError(message)
