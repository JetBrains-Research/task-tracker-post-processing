# Copyright (c) by anonymous author(s)

import csv
import logging
from typing import List, Tuple, Optional

import pandas as pd

from src.main.util import consts
from src.main.util.log_util import log_and_raise_error
from src.main.preprocessing import activity_tracker_handler as ath
from src.main.preprocessing.code_tracker_handler import handle_ct_file
from src.main.preprocessing.activity_tracker_handler import handle_ati_file, get_ct_name_from_ati_data, \
    get_files_from_ati
from src.main.util.file_util import get_original_file_name, get_all_file_system_items, data_subdirs_condition, \
    get_parent_folder_name, get_output_directory, write_result, extension_file_condition, user_subdirs_condition

log = logging.getLogger(consts.LOGGER_NAME)


def is_ct_file(csv_file: str, column: consts.CODE_TRACKER_COLUMN = consts.CODE_TRACKER_COLUMN.CHOSEN_TASK) -> bool:
    with open(csv_file, encoding=consts.ISO_ENCODING) as f:
        reader = csv.reader(f)
        try:
            if column.value in next(reader):
                return True
        except StopIteration:
            return False
    return False


def __get_real_ati_file_index(files: List[str]) -> int:
    count_ati = 0
    ati_index = -1
    for i, f in enumerate(files):
        if consts.ACTIVITY_TRACKER_FILE_NAME in f and not is_ct_file(f):
            count_ati += 1
            ati_index = i
            if count_ati >= 2:
                log_and_raise_error('The number of activity tracker files is more than 1', log)
    return ati_index


def __has_files_with_same_names(files: List[str]) -> bool:
    original_files = list(map(get_original_file_name, files))
    return len(original_files) != len(set(original_files))


def __separate_ati_and_other_files(files: List[str]) -> Tuple[List[str], Optional[str]]:
    ati_file_index = __get_real_ati_file_index(files)
    ati_file = None
    if ati_file_index != -1:
        ati_file = files[ati_file_index]
        del files[ati_file_index]
    if __has_files_with_same_names(files):
        log.info('The number of the code tracker files with the same names is more than 1')
        ati_file = None
    return files, ati_file


def handle_ct_and_at(ct_file: str, ct_df: pd.DataFrame, ati_df: pd.DataFrame,
                     language: consts.LANGUAGE = consts.LANGUAGE.PYTHON) -> pd.DataFrame:
    files_from_at = None
    if ati_df is not None:
        try:
            files_from_at = get_files_from_ati(ati_df)
        except ValueError:
            ati_df = None

    ct_df[consts.CODE_TRACKER_COLUMN.FILE_NAME.value], does_contain_ct_name \
        = get_ct_name_from_ati_data(ct_file, language, files_from_at)
    if ati_df is not None and does_contain_ct_name:
        ct_df = ath.merge_code_tracker_and_activity_tracker_data(ct_df, ati_df)
        return ct_df

    ati_new_data = pd.DataFrame(ath.get_full_default_columns_for_at(ct_df.shape[0]))
    ct_df = ct_df.join(ati_new_data)
    return ct_df


def merge_ct_with_ati(path: str, to_filter_ati_data: bool = True) -> str:
    output_directory = get_output_directory(path, consts.MERGING_CT_AND_ATI_OUTPUT_DIRECTORY)
    user_folders = get_all_file_system_items(path, user_subdirs_condition, consts.FILE_SYSTEM_ITEM.SUBDIR)
    for user_folder in user_folders:
        log.info(f'Start handling the folder {user_folder}')
        task_folders = get_all_file_system_items(user_folder, item_type=consts.FILE_SYSTEM_ITEM.SUBDIR)
        for task_folder in task_folders:
            log.info(f'Start handling the folder {task_folder}')
            files = get_all_file_system_items(task_folder, extension_file_condition(consts.EXTENSION.CSV))
            try:
                ct_files, ati_file = __separate_ati_and_other_files(files)
            # Drop the current folder
            except ValueError:
                continue

            ati_df = handle_ati_file(ati_file, to_filter_ati_data)
            for ct_file in ct_files:
                ct_df, language = handle_ct_file(ct_file)
                ct_df = handle_ct_and_at(ct_file, ct_df, ati_df, language)
                write_result(output_directory, path, ct_file, ct_df)

        log.info(f'Finish handling the folder {user_folder}')
    return output_directory
