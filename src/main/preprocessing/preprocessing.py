# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from typing import List, Tuple

import pandas as pd

from src.main.util import consts
from src.main.util.consts import EXTENSION, CODE_TRACKER_COLUMN, TEST_MODE, ACTIVITY_TRACKER_COLUMN, \
    ACTIVITY_TRACKER_FILE_NAME
from src.main.util.file_util import get_output_directory, get_all_file_system_items, all_items_condition, \
    extension_file_condition, get_file_with_max_size, create_directory, get_name_from_path, create_file, \
    get_content_from_file

log = logging.getLogger(consts.LOGGER_NAME)


def __partition_into_ct_and_ati_files(files: List[str]) -> Tuple[List[str], List[str]]:
    ati_files = [f for f in files if ACTIVITY_TRACKER_FILE_NAME in f]
    ct_files = [f for f in files if f not in ati_files]
    return ct_files, ati_files


def __merge_ati_files(ati_files: List[str]) -> pd.DataFrame:
    ati_df = pd.DataFrame(columns=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    for ati_file in ati_files:
        current_ati_df = pd.read_csv(ati_file, encoding=consts.ISO_ENCODING,
                                     names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
        ati_df = ati_df.append(current_ati_df, ignore_index=True)
    ati_df.drop_duplicates(keep='first')
    ati_df.sort_values(by=[ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value])
    return ati_df


def is_test_mode(ct_df: pd.DataFrame) -> bool:
    return ct_df[CODE_TRACKER_COLUMN.TEST_MODE.value].values[0] == TEST_MODE.ON.value


# The function returns True if the code tracker file was created and False otherwise
def __handle_ct_files(ct_files: List[str], output_task_path: str) -> bool:
    max_ct_file = get_file_with_max_size(ct_files)
    if max_ct_file:
        new_ct_path = os.path.join(output_task_path, get_name_from_path(max_ct_file))
        ct_df = pd.read_csv(max_ct_file)
        if not is_test_mode(ct_df):
            create_file(get_content_from_file(max_ct_file), new_ct_path)
            return True
    return False


# Merge ide-events files
# Delete unnecessary code tracker files
# Delete files with test mode = ON
def preprocess_data(path: str) -> str:
    output_directory = get_output_directory(path, consts.PREPROCESSING_DIRECTORY)
    user_folders = get_all_file_system_items(path, lambda dir: 'user' in dir, consts.FILE_SYSTEM_ITEM.SUBDIR)
    for user_folder in user_folders:
        user_path = os.path.join(path, get_name_from_path(user_folder, with_extension=False))
        output_user_path = os.path.join(output_directory, get_name_from_path(user_folder, False))
        log.info(f'Start handling the path {user_path}')
        task_folders = get_all_file_system_items(user_path, all_items_condition, consts.FILE_SYSTEM_ITEM.SUBDIR)
        for task_folder in task_folders:
            task_path = os.path.join(user_path, get_name_from_path(task_folder, with_extension=False))
            output_task_path = os.path.join(output_user_path, get_name_from_path(task_folder, False))
            log.info(f'Start handling the folder {task_path}')
            files = get_all_file_system_items(task_path, extension_file_condition(EXTENSION.CSV))
            ct_files, ati_files = __partition_into_ct_and_ati_files(files)
            if __handle_ct_files(ct_files, output_task_path) and ati_files:
                new_ati_path = os.path.join(output_task_path, get_name_from_path(ati_files[0]))
                __merge_ati_files(ati_files).to_csv(new_ati_path)
    return output_directory
