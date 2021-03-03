# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

import pandas as pd

from src.main.task_scoring.task_scoring import unpack_tests_results as utr
from src.main.util import consts
from src.main.util.consts import FILE_SYSTEM_ITEM
from src.main.util.data_util import handle_folder
from src.main.util.file_util import get_all_file_system_items, get_output_directory, language_item_condition, \
    get_name_from_path
from src.main.util.log_util import log_and_raise_error

log = logging.getLogger(consts.LOGGER_NAME)

TESTS_RESULT = consts.TASK_TRACKER_COLUMN.TESTS_RESULTS.value
FILE_NAME = consts.TASK_TRACKER_COLUMN.FILE_NAME.value
TASK = consts.TASK_TRACKER_COLUMN.TASK.value


def __get_current_score(tests_results: str, current_task_key: str) -> float:
    tasks = consts.TASK.tasks()
    current_task_index = consts.TASK.tasks().index(consts.TASK(current_task_key))
    if current_task_index == -1:
        log_and_raise_error(f'Undefined task: {current_task_key}', log)
    return utr(tests_results, tasks)[current_task_index]


def __get_current_task_key(df: pd.DataFrame) -> str:
    key = get_name_from_path(df.iloc[0][FILE_NAME], with_extension=False)
    # Old name from old data
    if key == 'zero':
        key = 'is_zero'
    return consts.TASK(key).value


def __unpack_tests_results(df: pd.DataFrame) -> pd.DataFrame:
    df[TASK] = __get_current_task_key(df)
    df[TESTS_RESULT] = df.apply(lambda row: __get_current_score(row[TESTS_RESULT], row[TASK]), axis=1)
    return df


def unpack_tests_results(path: str, output_directory_prefix: str = 'unpack_tests_results') -> str:
    """
    This function allows to unpack tests results from array like [-1, -1, -1, -1, -1, -1] into score:
    -1, or a number in [0, 1]

    Also this function allows to add a new column TASK with task key
    """
    languages = get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
    output_directory = get_output_directory(path, output_directory_prefix)
    for _ in languages:
        handle_folder(path, output_directory_prefix, __unpack_tests_results)
    return output_directory
