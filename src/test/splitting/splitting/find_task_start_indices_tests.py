# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import unittest
from typing import List

import pandas as pd

from src.main.util import consts
from src.main.splitting.splitting import find_task_start_indices
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT

PIES_COUNT_1 = 2
PIES_COUNT_2 = 3
PIES_COUNT_3 = 2
IS_ZERO_COUNT_1 = 2
IS_ZERO_COUNT_2 = 4

START_INDEX_1 = 0
START_INDEX_2 = 4
START_INDEX_3 = 11


def __get_chosen_tasks() -> List[str]:
    return [consts.TASK.PIES.value] * PIES_COUNT_1 + [consts.TASK.ZERO.value] * IS_ZERO_COUNT_1 + \
           [consts.TASK.PIES.value] * PIES_COUNT_2 + [consts.TASK.ZERO.value] * IS_ZERO_COUNT_2 + \
           [consts.TASK.PIES.value] * PIES_COUNT_3


def get_df() -> pd.DataFrame:
    return pd.DataFrame({consts.CODE_TRACKER_COLUMN.CHOSEN_TASK.value: __get_chosen_tasks()})


def crop_first_pies(df: pd.DataFrame, n: int = PIES_COUNT_1) -> pd.DataFrame:
    return df[n:]


def crop_last_pies(df: pd.DataFrame, n: int = PIES_COUNT_3) -> pd.DataFrame:
    return df[:-n]


class TestStartIndexFinding(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def find_and_check_start_indices(self, df: pd.DataFrame, expected_indices: List[int]) -> None:
        actual_indices = find_task_start_indices(df, consts.TASK.PIES)
        self.assertEqual(expected_indices, actual_indices)

    # Finding start indices in:
    #
    #   chosenTask
    # 0     pies
    # 1     pies
    # 2     is_zero
    # 3     is_zero
    # 4     pies
    # 5     pies
    # 6     pies
    # 7     is_zero
    # 8     is_zero
    # 9     is_zero
    # 10    is_zero
    # 11    pies
    # 12    pies
    def test_finding_start_indices_everywhere(self) -> None:
        self.find_and_check_start_indices(get_df(), [START_INDEX_1, START_INDEX_2, START_INDEX_3])

    # Finding start indices in:
    #
    #   chosenTask
    # 2     is_zero
    # 3     is_zero
    # 4     pies
    # 5     pies
    # 6     pies
    # 7     is_zero
    # 8     is_zero
    # 9     is_zero
    # 10    is_zero
    def test_finding_start_indices_in_the_middle(self) -> None:
        self.find_and_check_start_indices(crop_last_pies(crop_first_pies(get_df())), [START_INDEX_2])

    # Finding start indices in:
    #
    #   chosenTask
    # 0     pies
    # 1     pies
    # 2     is_zero
    # 3     is_zero
    # 4     pies
    # 5     pies
    # 6     pies
    # 7     is_zero
    # 8     is_zero
    # 9     is_zero
    # 10    is_zero
    def test_finding_start_indices_at_the_beginning(self) -> None:
        self.find_and_check_start_indices(crop_last_pies(get_df()), [START_INDEX_1, START_INDEX_2])

    # Finding start indices in:
    #
    #   chosenTask
    # 2     is_zero
    # 3     is_zero
    # 4     pies
    # 5     pies
    # 6     pies
    # 7     is_zero
    # 8     is_zero
    # 9     is_zero
    # 10    is_zero
    # 11    pies
    # 12    pies
    def test_finding_start_indices_at_the_end(self) -> None:
        self.find_and_check_start_indices(crop_first_pies(get_df()), [START_INDEX_2, START_INDEX_3])

    # Finding start indices in:
    #
    #   chosenTask
    # 0     pies
    # 1     pies
    def test_finding_start_indices_in_full_df(self):
        self.find_and_check_start_indices(crop_last_pies(get_df(), -PIES_COUNT_1), [START_INDEX_1])

    # Finding start indices in:
    #
    #   chosenTask
    # 7     is_zero
    # 8     is_zero
    # 9     is_zero
    # 10    is_zero
    def test_finding_start_indices_in_empty_df(self):
        self.find_and_check_start_indices(crop_last_pies(crop_first_pies(get_df(), PIES_COUNT_1 + IS_ZERO_COUNT_1 + PIES_COUNT_2)), [])
