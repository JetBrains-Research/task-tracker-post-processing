# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

from enum import Enum
from typing import List

from src.main.processing.preprocessing import preprocess_data
from src.main.task_scoring.tasks_tests_handler import run_tests
from src.main.processing.merging_tt_with_ati import merge_tt_with_ati
from src.main.task_scoring.task_scoring import reorganize_files_structure
from src.main.processing.int_experience_adding import add_int_experience
from src.main.processing.intermediate_diffs_removing import remove_intermediate_diffs
from src.main.processing.inefficient_statements_removing import remove_inefficient_statements


class PLOT_TYPE(Enum):
    PARTICIPANTS_DISTRIBUTION = 'participants_distr'
    TASKS_DISTRIBUTION = 'tasks_distr'
    ATI_PLOTS = 'ati'
    SCORING_SOLUTIONS = 'scoring'

    @classmethod
    def plot_types(cls) -> List[PLOT_TYPE]:
        return [_ for _ in PLOT_TYPE]

    @classmethod
    def values(cls) -> List[str]:
        return [p_t.value for p_t in PLOT_TYPE]

    @classmethod
    def description(cls) -> str:
        return f'{PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value} - visualize participants distribution; ' \
               f'{PLOT_TYPE.TASKS_DISTRIBUTION.value} - visualize tasks distribution; ' \
               f'{PLOT_TYPE.ATI_PLOTS.value} - visualize activity tracker plots; ' \
               f'{PLOT_TYPE.SCORING_SOLUTIONS.value} - visualize scoring of the solutions;'

    @classmethod
    def str_to_plot_type(cls, value: str) -> PLOT_TYPE:
        try:
            return PLOT_TYPE(value.lower())
        except ValueError:
            raise ValueError(f'{value} is not a plot_type value. Available values: {PLOT_TYPE.description()}')


# Todo: create an interface for such kind of classes?
class PROCESSING_LEVEL(Enum):
    PRIMARY = 0
    MERGE = 1
    TESTS_RESULTS = 2
    REORGANIZE = 3
    INTERMEDIATE_DIFFS = 4
    INEFFICIENT_STATEMENTS = 5
    INT_EXPERIENCE = 6

    @property
    def __level_actions(self):
        return {
            self.PRIMARY: preprocess_data,
            self.MERGE: merge_tt_with_ati,
            self.TESTS_RESULTS: run_tests,
            self.REORGANIZE: reorganize_files_structure,
            self.INTERMEDIATE_DIFFS: remove_intermediate_diffs,
            self.INEFFICIENT_STATEMENTS: remove_inefficient_statements,
            self.INT_EXPERIENCE: add_int_experience
        }

    def level_handler(self):
        return self.__level_actions[self]

    @classmethod
    def min_value(cls) -> int:
        return min([a_t.value for a_t in PROCESSING_LEVEL])

    @classmethod
    def max_value(cls) -> int:
        return max([a_t.value for a_t in PROCESSING_LEVEL])

    @classmethod
    def description(cls) -> str:
        return f'the Nth level runs all the level before it; ' \
               f'{PROCESSING_LEVEL.PRIMARY.value} - primary data processing; ' \
               f'{PROCESSING_LEVEL.MERGE.value} - merge activity-tracker and task-tracker files; ' \
               f'{PROCESSING_LEVEL.TESTS_RESULTS.value} - find tests results for the tasks; ' \
               f'{PROCESSING_LEVEL.REORGANIZE.value} - reorganize files structure; ' \
               f'{PROCESSING_LEVEL.INTERMEDIATE_DIFFS.value} - remove intermediate diffs; ' \
               f'{PROCESSING_LEVEL.INEFFICIENT_STATEMENTS.value} - [only for Python language] remove inefficient statements; ' \
               f'{PROCESSING_LEVEL.INT_EXPERIENCE.value} - add int experience column; '


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
    def params(cls) -> List[ALGO_PARAMS]:
        return [p for p in ALGO_PARAMS]


class PROCESSING_PARAMS(Enum):
    LEVEL = '--level'
    PATH = 'path'

    @classmethod
    def params(cls) -> List[PROCESSING_PARAMS]:
        return [p for p in PROCESSING_PARAMS]


class PLOTS_PARAMS(Enum):
    PATH = 'path'
    PLOT_TYPE = 'plot_type'
    TYPE_DISTR = '--type_distr'
    CHART_TYPE = '--chart_type'
    TO_UNION_RARE = '--to_union_rare'
    FORMAT = '--format'
    AUTO_OPEN = '--auto_open'

    @classmethod
    def params(cls) -> List[PLOTS_PARAMS]:
        return [p for p in PLOTS_PARAMS]
