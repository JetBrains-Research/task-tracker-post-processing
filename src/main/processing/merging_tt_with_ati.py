# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import csv
import logging
from typing import List, Tuple, Optional

import pandas as pd

from src.main.util import consts
from src.main.util.log_util import log_and_raise_error
from src.main.processing import activity_tracker_handler as ath
from src.main.processing.task_tracker_handler import handle_tt_file
from src.main.processing.activity_tracker_handler import handle_ati_file, get_tt_name_from_ati_data, \
    get_files_from_ati
from src.main.util.file_util import get_original_file_name, get_all_file_system_items, get_output_directory, \
    write_result, extension_file_condition, user_subdirs_condition

log = logging.getLogger(consts.LOGGER_NAME)


def is_tt_file(csv_file: str, column: consts.TASK_TRACKER_COLUMN = consts.TASK_TRACKER_COLUMN.CHOSEN_TASK) -> bool:
    """
    Check if the file is a task-tracker file.
    To do this, let's try to create a data frame with columns of the task-tracker file.
    If it didn't work, then the file is not a task-tracker file.
    """
    with open(csv_file, encoding=consts.ISO_ENCODING) as f:
        reader = csv.reader(f)
        try:
            if column.value in next(reader):
                return True
        except StopIteration:
            return False
    return False


def __get_real_ati_file_index(files: List[str]) -> int:
    """
    Find the index of the activity tracker file and return it.
    If there are more than one active tracker files in the folder, then throw an exception.
    If there is no such a file, then return -1.
    """
    count_ati = 0
    ati_index = -1
    for i, f in enumerate(files):
        if consts.ACTIVITY_TRACKER_FILE_NAME in f and not is_tt_file(f):
            count_ati += 1
            ati_index = i
            if count_ati >= 2:
                log_and_raise_error('The number of activity tracker files is more than 1', log)
    return ati_index


def __has_files_with_same_names(files: List[str]) -> bool:
    original_files = list(map(get_original_file_name, files))
    return len(original_files) != len(set(original_files))


def __separate_ati_and_tt_files(files: List[str]) -> Tuple[List[str], Optional[str]]:
    """
    Find the activity tracker file and separate it from the task-tracker files.
    """
    ati_file_index = __get_real_ati_file_index(files)
    ati_file = None
    if ati_file_index != -1:
        ati_file = files[ati_file_index]
        del files[ati_file_index]
    # We assume that by this step the processing (see processing.py) has already been completed,
    # so there should not be several files with the same name.
    if __has_files_with_same_names(files):
        log.info('The number of the code tracker files with the same names is more than 1')
        ati_file = None
    return files, ati_file


def handle_tt_and_at(tt_file: str, tt_df: pd.DataFrame, ati_df: pd.DataFrame,
                     language: consts.LANGUAGE = consts.LANGUAGE.PYTHON) -> pd.DataFrame:
    """
    Try to find the current task-tracker file among the files tracked by the activity tracker plugin.
    If this file was found, combine the active tracker data with the task-tracker data.
    If no activities were found for the given task-tracker file,
    fill the information about events in IDE with empty values.
    """
    files_from_at = None
    if ati_df is not None:
        try:
            files_from_at = get_files_from_ati(ati_df)
        except ValueError:
            ati_df = None

    tt_df[consts.TASK_TRACKER_COLUMN.FILE_NAME.value], does_contain_tt_name \
        = get_tt_name_from_ati_data(tt_file, language, files_from_at)
    if ati_df is not None and does_contain_tt_name:
        tt_df = ath.merge_task_tracker_and_activity_tracker_data(tt_df, ati_df)
        return tt_df

    ati_new_data = pd.DataFrame(ath.get_full_default_columns_for_at(tt_df.shape[0]))
    tt_df = tt_df.join(ati_new_data)
    return tt_df


def merge_tt_with_ati(path: str, to_filter_ati_data: bool = True) -> str:
    """
    At this stage, merging data from the task-tracker plugin and activity tracker plugin takes place.
    Code snapshots that did not find activity tracker events are assigned empty values.

    For more details see
    https://github.com/JetBrains-Research/codetracker-data/wiki/Data-preprocessing:-merge-activity-tracker-and-code-tracker-files
    """
    output_directory = get_output_directory(path, consts.MERGING_TT_AND_ATI_OUTPUT_DIRECTORY)
    user_folders = get_all_file_system_items(path, user_subdirs_condition, consts.FILE_SYSTEM_ITEM.SUBDIR)
    for user_folder in user_folders:
        log.info(f'Start handling the folder {user_folder}')
        task_folders = get_all_file_system_items(user_folder, item_type=consts.FILE_SYSTEM_ITEM.SUBDIR)
        for task_folder in task_folders:
            log.info(f'Start handling the folder {task_folder}')
            files = get_all_file_system_items(task_folder, extension_file_condition(consts.EXTENSION.CSV))
            try:
                tt_files, ati_file = __separate_ati_and_tt_files(files)
            # Skip the current folder
            except ValueError:
                continue

            ati_df = handle_ati_file(ati_file, to_filter_ati_data)
            for tt_file in tt_files:
                tt_df, language = handle_tt_file(tt_file)
                tt_df = handle_tt_and_at(tt_file, tt_df, ati_df, language)
                write_result(output_directory, path, tt_file, tt_df)

        log.info(f'Finish handling the folder {user_folder}')
    return output_directory
