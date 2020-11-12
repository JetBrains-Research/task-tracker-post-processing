# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import ast
import logging
from typing import List, Union

import pandas as pd

from src.main.util import consts
from src.main.util.consts import TASK
from src.main.util.log_util import log_and_raise_error
from src.main.util.file_util import get_all_file_system_items, ct_file_condition, get_output_directory, \
    get_name_from_path, get_parent_folder, copy_file, get_parent_folder_name

log = logging.getLogger(consts.LOGGER_NAME)

CHOSEN_TASK = consts.CODE_TRACKER_COLUMN.CHOSEN_TASK.value
TASK_STATUS = consts.CODE_TRACKER_COLUMN.TASK_STATUS.value
TESTS_RESULTS = consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value


def unpack_tests_results(tests_results: str, tasks: List[TASK]) -> List[float]:
    tests_results = ast.literal_eval(tests_results)
    if len(tests_results) != len(tasks):
        log_and_raise_error(f'Cannot identify tasks because of'
                            f' unexpected tests_results length: {len(tests_results)}', log)
    return tests_results


def get_solved_task(tests_results: str) -> Union[TASK, consts.DEFAULT_VALUE]:
    tasks = consts.TASK.tasks()
    tests_results = unpack_tests_results(tests_results, tasks)
    solved_tasks = [t for i, t in enumerate(tasks) if tests_results[i] == 1]
    if len(solved_tasks) == 0:
        log.info(f'No solved tasks found, tests results: {tests_results}')
        return consts.DEFAULT_VALUE.TASK
    elif len(solved_tasks) == 1:
        log.info(f'Found solved task {solved_tasks[0]}, tests results: {tests_results}')
        return solved_tasks[0]
    else:
        log_and_raise_error(f'Several tasks are solved: {solved_tasks}, tests results: {tests_results}', log)


def find_splits(ct_df: pd.DataFrame) -> pd.DataFrame:
    # Fill chosen task according to solved task
    ct_df[CHOSEN_TASK] = ct_df.apply(lambda row: get_solved_task(row[TESTS_RESULTS]).value, axis=1)

    # Change task status according to chosen task
    ct_df.loc[ct_df[CHOSEN_TASK].isnull(), TASK_STATUS] = consts.DEFAULT_VALUE.TASK_STATUS.value
    ct_df.loc[ct_df[CHOSEN_TASK].notnull(), TASK_STATUS] = consts.TASK_STATUS.SOLVED.value

    # Backward fill chosen task
    ct_df[CHOSEN_TASK] = ct_df[CHOSEN_TASK].bfill()
    return ct_df


# To find start index for each group of rows with the same task
def find_task_start_indices(df: pd.DataFrame, task: consts.TASK) -> List[int]:
    # An index is the start index for some task, if CHOSEN_TASK at this index equals task, but at index-1 -- doesn't,
    # So we should compare it with shifted dataframe
    return df.index[(df[CHOSEN_TASK] == task.value) & (df[CHOSEN_TASK].shift(1) != task.value)].tolist()


def find_task_dfs(df: pd.DataFrame, task: consts.TASK) -> List[pd.DataFrame]:
    start_indices = find_task_start_indices(df, task)
    split_indices = zip(start_indices, start_indices[1:] + [df.shape[0]])
    # Split df into several dfs with only one group of rows with the same task
    split_dfs = [df[start_index:end_index] for start_index, end_index in split_indices]
    # In each df find this group of rows with the same task
    return [split_df[split_df[CHOSEN_TASK] == task.value] for split_df in split_dfs]


def __get_dst_path(src_file: str, output_directory: str) -> str:
    file_name = get_name_from_path(src_file)
    task_path = get_parent_folder(src_file)
    task = get_name_from_path(task_path, with_extension=False)
    language = get_parent_folder_name(task_path)
    return os.path.join(output_directory, language, task, file_name)


def reorganize_files_structure(path: str, output_directory_suffix: str = 'separated_tasks') -> str:
    """
    3.0 version: reorganize the file structure
    Before the function calling:

    -root
     --user_N1
      ---task1
       ----user_N1_files
     --user_N2
      ---task1
       ----user_N2_files

    After the function calling:

    -root
     --task1
      ----user_N1_files
      ----user_N2_files

    For more details see https://github.com/JetBrains-Research/codetracker-data/wiki/Data-preprocessing:-reorganize-files-structure
    """
    output_directory = get_output_directory(path, output_directory_suffix)
    files = get_all_file_system_items(path, ct_file_condition)
    for file in files:
        log.info(f'Start splitting file {file}')
        dst_path = __get_dst_path(file, output_directory)
        log.info(f'Destination for the file {file} is {dst_path}')
        copy_file(file, dst_path)
    return output_directory
