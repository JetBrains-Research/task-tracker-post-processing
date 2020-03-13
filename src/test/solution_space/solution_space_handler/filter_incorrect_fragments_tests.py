# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import unittest
import pandas as pd

from src.main.solution_space.solution_space_handler import __filter_incorrect_fragments
from src.main.util.consts import LOGGER_NAME, LOGGER_TEST_FILE, LOGGER_FORMAT, TASK, CODE_TRACKER_COLUMN

log = logging.getLogger(LOGGER_NAME)

INCORRECT = '[-1,-1,-1,-1,-1,-1]'
CORRECT = '[-1,1,0.5,0.5,-1,-1]'
LESS_TASKS = '[-1,-1]'

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


def run_test(before_filtering: pd.DataFrame, expected_after_filtering: pd.DataFrame) -> bool:
    try:
        actual_after_filtering = __filter_incorrect_fragments(before_filtering)
        actual_after_filtering.index = [*range(actual_after_filtering.shape[0])]
    except ValueError:
        return False
    return actual_after_filtering.equals(expected_after_filtering)


def clear_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.iloc[0:0]


class TestTimeMethods(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_all_correct(self):
        before_filter_df = pd.DataFrame(ALL_CORRECT)
        expected_after_filter_df = pd.DataFrame(ALL_CORRECT)
        self.assertTrue(run_test(before_filter_df, expected_after_filter_df))

    def test_all_incorrect(self):
        before_filter_df = pd.DataFrame(ALL_INCORRECT)
        expected_after_filter_df = clear_df(before_filter_df.copy())
        self.assertTrue(run_test(before_filter_df, expected_after_filter_df))

    def test_all_mixed(self):
        before_filter_df = pd.DataFrame(MIXED)
        expected_after_filter_df = pd.DataFrame(MIXED_FILTERED)
        self.assertTrue(run_test(before_filter_df, expected_after_filter_df))

    def test_incorrect_data(self):
        before_filter_df = pd.DataFrame(INCORRECT_DATA)
        expected_after_filter_df = pd.DataFrame(INCORRECT_DATA)
        self.assertEqual(run_test(before_filter_df, expected_after_filter_df), False)

