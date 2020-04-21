# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from os import path
from typing import List

import pandas as pd

from src.main.util import consts
from src.test.test_util import LoggedTest
from src.main.splitting.splitting import find_task_dfs
from src.main.util.file_util import get_all_file_system_items

TEST_DATA_FOLDER = path.join(consts.TEST_DATA_PATH, 'splitting/splitting/')
DF_FILE = path.join(TEST_DATA_FOLDER, 'df_to_split.csv')


def get_expected_task_dfs(task: consts.TASK) -> List[pd.DataFrame]:
    df_files = sorted(get_all_file_system_items(TEST_DATA_FOLDER, (lambda n: task.value in n)))
    return [pd.read_csv(df_file, encoding=consts.ISO_ENCODING) for df_file in df_files]


class TestFindingTaskDfs(LoggedTest):

    def testFindingTaskDfs(self) -> None:
        df = pd.read_csv(DF_FILE, encoding=consts.ISO_ENCODING)
        for task in consts.TASK:
            actual_task_dfs = list(map(lambda task_df: task_df.sort_index(inplace=True), find_task_dfs(df, task)))
            expected_tasks_dfs = list(map(lambda task_df: task_df.sort_index(inplace=True), get_expected_task_dfs(task)))
            self.assertEqual(actual_task_dfs, expected_tasks_dfs)