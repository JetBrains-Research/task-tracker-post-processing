# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from typing import List, Tuple, Optional

import pandas as pd

from src.main.util import consts
from src.main.util.consts import EXTENSION, TASK_TRACKER_COLUMN, TEST_MODE, ACTIVITY_TRACKER_COLUMN, \
    ACTIVITY_TRACKER_FILE_NAME
from src.main.util.file_util import get_output_directory, get_all_file_system_items, all_items_condition, \
    extension_file_condition, get_name_from_path, create_file, user_subdirs_condition

log = logging.getLogger(consts.LOGGER_NAME)


def __partition_into_tt_and_ati_files(files: List[str]) -> Tuple[List[str], List[str]]:
    ati_files = [f for f in files if ACTIVITY_TRACKER_FILE_NAME in f]
    ct_files = [f for f in files if f not in ati_files]
    return ct_files, ati_files


def __merge_dataframes(dataframes: List[pd.DataFrame], empty_df: pd.DataFrame = pd.DataFrame(),
                       sorted_column: Optional[str] = None) -> pd.DataFrame:
    """
    Combine all dataframes according to timestamps, excluding duplicates.
    """
    for df in dataframes:
        empty_df = empty_df.append(df, ignore_index=True)
    empty_df.drop_duplicates(keep='first')
    if sorted_column is not None:
        empty_df.sort_values(by=[sorted_column])
    return empty_df


def __merge_ati_files(ati_files: List[str]) -> pd.DataFrame:
    """
    Combine all activity tracker files according to timestamps, excluding duplicates.
    """
    ati_df = pd.DataFrame(columns=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    dataframes = []
    for ati_file in ati_files:
        dataframes.append(pd.read_csv(ati_file, encoding=consts.ISO_ENCODING,
                                      names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns()))
    return __merge_dataframes(dataframes, ati_df, ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value)


def is_test_mode(ct_df: pd.DataFrame) -> bool:
    # The old version of the data does not contains the test mode column. We should handle this case correctly anyway.
    if TASK_TRACKER_COLUMN.TEST_MODE.value not in ct_df.columns:
        return False
    return ct_df[TASK_TRACKER_COLUMN.TEST_MODE.value].values[0] == TEST_MODE.ON.value


def __handle_tt_files(tt_files: List[str], output_task_path: str) -> bool:
    """
    The function returns True if new task-tracker file was created and False otherwise
    We should choose the last state of the task-tracker files for the task or all last states and create a new file
    where we union them. The student can submit the solution several times, while the history of the task-tracker file
    is not erased. In this way, we only need to select the final file with the entire history. On the other hand,
    if the file was full, then it will be sent additionally and new files will contain a new history.
    In this case, it is necessary to find the last states of all files with a unique history, combine according to
    timestamps and write to a new final file.

    For more details see https://github.com/JetBrains-Research/codetracker-data/wiki/Data-preprocessing:-primary-data-processing
    """
    dataframes = []
    file_name = None
    for tt_file in tt_files:
        current_df = pd.read_csv(tt_file, encoding=consts.ISO_ENCODING)
        if not is_test_mode(current_df):
            dataframes.append(current_df)
            if file_name is None:
                file_name = get_name_from_path(tt_file)
    if len(dataframes) == 0:
        return False
    new_tt_path = os.path.join(output_task_path, file_name)
    create_file("", new_tt_path)
    __merge_dataframes(dataframes, sorted_column=TASK_TRACKER_COLUMN.TIMESTAMP.value).to_csv(new_tt_path)
    return True


def preprocess_data(path: str) -> str:
    """
    We use task-tracker plugin (see https://github.com/JetBrains-Research/task-tracker-plugin)
    and activity tracker plugin (see https://plugins.jetbrains.com/plugin/8126-activity-tracker)
    to gather the source data. The data gathering consists of us collecting code snapshots and actions during
    the solving of various programming tasks by students. The data also contains information about the age,
    programming experience and so on of the student (student profile), and the current task that the student is solving.

    - At this stage, the test files that were created during the testing phase are deleted. They have ON value in the
    test mode column in the task-tracker file.
    - Also, the student could send several files with the history of solving the task, each of which can include
    the previous ones. At this stage, unnecessary files are deleted. Ultimately, there is only one file with a unique
    history of solving the current problem.
    - In addition, for each task-tracker file, a unique file of the activity tracker is sent. In this step,
    all files of the activity tracker are combined into one.

    For more details see https://github.com/JetBrains-Research/codetracker-data/wiki/Data-preprocessing:-primary-data-processing
    """
    output_directory = get_output_directory(path, consts.PREPROCESSING_DIRECTORY)
    user_folders = get_all_file_system_items(path, user_subdirs_condition, consts.FILE_SYSTEM_ITEM.SUBDIR)
    for user_folder in user_folders:
        output_user_path = os.path.join(output_directory, get_name_from_path(user_folder, False))
        log.info(f'Start handling the path {user_folder}')
        task_folders = get_all_file_system_items(user_folder, all_items_condition, consts.FILE_SYSTEM_ITEM.SUBDIR)
        for task_folder in task_folders:
            output_task_path = os.path.join(output_user_path, get_name_from_path(task_folder, False))
            log.info(f'Start handling the folder {task_folder}')
            files = get_all_file_system_items(task_folder, extension_file_condition(EXTENSION.CSV))
            tt_files, ati_files = __partition_into_tt_and_ati_files(files)
            if __handle_tt_files(tt_files, output_task_path) and ati_files:
                new_ati_path = os.path.join(output_task_path, get_name_from_path(ati_files[0]))
                __merge_ati_files(ati_files).to_csv(new_ati_path)
    return output_directory
