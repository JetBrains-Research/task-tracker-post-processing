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


class ALGO_PARAMS(Enum):
    CONSTRUCT = '--construct'
    DESERIALIZE = '--deserialize'
    SERIALIZE = '--serialize'
    VISUALIZE = '--viz'
    NOD_NUM_STAT = '--nod_num_stat'
    TASK = '--task'
    LEVEL = '--level'
    PATH = 'path'

    @classmethod
    def params(cls) -> List['ALGO_PARAMS']:
        return [p for p in ALGO_PARAMS]


class PREPROCESSING_PARAMS(Enum):
    LEVEL = '--level'
    PATH = 'path'

    @classmethod
    def params(cls) -> List['PREPROCESSING_PARAMS']:
        return [p for p in PREPROCESSING_PARAMS]


class PLOTS_PARAMS(Enum):
    PATH = 'path'
    PLOT_TYPE = 'plot_type'
    TYPE_DISTR = '--type_distr'
    CHART_TYPE = '--chart_type'
    TO_UNION_RARE = '--to_union_rare'
    FORMAT = '--format'
    AUTO_OPEN = '--auto_open'

    @classmethod
    def params(cls) -> List['PLOTS_PARAMS']:
        return [p for p in PLOTS_PARAMS]
