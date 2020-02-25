import logging
import os
import unittest

import pandas as pd

from src.main.util import consts
from src.main.splitting.splitting import check_tasks_on_correct_fragments
from src.main.splitting.tasks_tests_handler import create_in_and_out_dict
from src.main.util.consts import LOGGER_TEST_FILE, TEST_DATA_PATH, TASK, LOGGER_FORMAT


class TestRunTests(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_find_real_splits_large(self):
        data = pd.read_csv(os.path.join(TEST_DATA_PATH, "splitting/splitting/Main.csv"))
        tasks = [t.value for t in TASK]
        in_and_out_files_dict = create_in_and_out_dict(tasks)

        _, result_data = check_tasks_on_correct_fragments(data, tasks, in_and_out_files_dict)
        actual_data = pd.read_csv(os.path.join(TEST_DATA_PATH, "splitting/splitting/Main_running_tests_result.csv"))

        actual_data[consts.CODE_TRACKER_COLUMN.FRAGMENT.value].fillna('', inplace=True)
        result_data[consts.CODE_TRACKER_COLUMN.FRAGMENT.value].fillna('', inplace=True)

        result_data[consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value] = result_data[consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value].astype(str)

        self.assertTrue(actual_data.equals(result_data))
