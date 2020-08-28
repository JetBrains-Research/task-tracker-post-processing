# Copyright (c) by anonymous author(s)

import logging
from typing import Callable, Tuple

import pytest
import pandas as pd

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.consts import LOGGER_NAME, CODE_TRACKER_COLUMN
from src.main.solution_space.solution_space_handler import __filter_incorrect_fragments

log = logging.getLogger(LOGGER_NAME)

INCORRECT = '[-1,-1,-1,-1,-1,-1]'
CORRECT = '[0,1,0.5,0.5,0,0]'
LESS_TASKS = '[-1,-1]'
ERROR = '[-1,1,0.5,0.5,-1,-1]'

ALL_CORRECT = {
    'Data': [1, 2, 3],
    CODE_TRACKER_COLUMN.TESTS_RESULTS.value: [CORRECT, CORRECT, CORRECT]
}

ALL_INCORRECT = {
    'Data': [1, 2, 3],
    CODE_TRACKER_COLUMN.TESTS_RESULTS.value: [INCORRECT, INCORRECT, INCORRECT]
}

MIXED = {
    'Data': [1, 2, 3],
    CODE_TRACKER_COLUMN.TESTS_RESULTS.value: [INCORRECT, CORRECT, INCORRECT]
}

MIXED_FILTERED = {
    'Data': [2],
    CODE_TRACKER_COLUMN.TESTS_RESULTS.value: [CORRECT]
}

INCORRECT_DATA = {
    'Data': [1, 2, 3],
    CODE_TRACKER_COLUMN.TESTS_RESULTS.value: [LESS_TASKS, LESS_TASKS, LESS_TASKS]
}

ERROR_DATA = {
    'Data': [1, 2, 3],
    CODE_TRACKER_COLUMN.TESTS_RESULTS.value: [ERROR, ERROR, ERROR]
}


def run_test(before_filtering: pd.DataFrame, expected_after_filtering: pd.DataFrame) -> bool:
    actual_after_filtering = __filter_incorrect_fragments(before_filtering)
    actual_after_filtering.index = [*range(actual_after_filtering.shape[0])]
    return actual_after_filtering.equals(expected_after_filtering)


def clear_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.iloc[0:0]


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestFilterIncorrectFragments:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (pd.DataFrame(ALL_CORRECT), pd.DataFrame(ALL_CORRECT)),
                        (pd.DataFrame(ALL_INCORRECT), clear_df(pd.DataFrame(ALL_INCORRECT).copy())),
                        (pd.DataFrame(MIXED), pd.DataFrame(MIXED_FILTERED))
                    ],
                    ids=[
                        'test_all_correct',
                        'test_all_incorrect',
                        'test_all_mixed'
                    ])
    def param_filter_incorrect_fragments_test(request) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return request.param

    def test_filter_incorrect_fragments(self, param_filter_incorrect_fragments_test: Callable) -> None:
        (before_filter_df, expected_after_filter_df) = param_filter_incorrect_fragments_test
        assert run_test(before_filter_df, expected_after_filter_df)

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (pd.DataFrame(INCORRECT_DATA), pd.DataFrame(INCORRECT_DATA)),
                        (pd.DataFrame(ERROR_DATA), pd.DataFrame(ERROR_DATA))
                    ],
                    ids=[
                        'test_incorrect_data',
                        'test_error_data'
                    ])
    def param_filter_incorrect_fragments_with_errors_test(request) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return request.param

    def test_filter_incorrect_fragments_with_errors(self,
                                                    param_filter_incorrect_fragments_with_errors_test: Callable) -> None:
        (before_filter_df, expected_after_filter_df) = param_filter_incorrect_fragments_with_errors_test
        with pytest.raises(ValueError):
            run_test(before_filter_df, expected_after_filter_df)
