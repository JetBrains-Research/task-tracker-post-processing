import csv
import logging
import os
from os import makedirs

import pandas as pd

from src.main.preprocessing.activity_tracker_handler import handle_at_file, get_ct_name_from_at_data, \
    get_files_from_ati
from src.main.preprocessing.code_tracker_handler import handle_ct_file
from src.main.preprocessing import activity_tracker_handler as ath
from src.main.util import consts
from src.main.util.file_util import get_original_file_name, get_all_file_system_items, data_subdirs_condition, \
    csv_file_condition, get_parent_folder, get_parent_folder_name, get_file_name_from_path, get_result_folder, \
    write_result

log = logging.getLogger(consts.LOGGER_NAME)


def __is_ct_file(csv_file: str):
    with open(csv_file, encoding=consts.ENCODING) as f:
        reader = csv.reader(f)
        try:
            if consts.CODE_TRACKER_COLUMN.CHOSEN_TASK.value in next(reader):
                return True
        except StopIteration:
            return False
    return False


def __get_real_at_file_index(files: list):
    count_at = 0
    at_index = -1
    for i, f in enumerate(files):
        if consts.ACTIVITY_TRACKER_FILE_NAME in f:
            count_at += 1
            if count_at >= 2:
                log.error('The number of activity tracker files is more than 1')
                raise ValueError('The number of activity tracker files is more than 1')
            if not __is_ct_file(f):
                at_index = i
    return at_index


def __has_files_with_same_names(files: list):
    original_files = list(map(get_original_file_name, files))
    return len(original_files) != len(set(original_files))


def __separate_at_and_other_files(files: list):
    at_file_index = __get_real_at_file_index(files)
    at_file = None
    if at_file_index != -1:
        at_file = files[at_file_index]
        del files[at_file_index]
    if __has_files_with_same_names(files):
        log.info('The number of the code tracker files with the same names is more than 1')
        at_file = None
    return files, at_file


def handle_ct_and_at(ct_file, ct_df, at_file, at_df, language):
    files_from_at = None
    if at_df is not None:
        try:
            files_from_at = get_files_from_ati(at_df)
        except ValueError:
            at_df = None

    ct_df[consts.CODE_TRACKER_COLUMN.FILE_NAME.value], does_contain_ct_name = get_ct_name_from_at_data(ct_file,
                                                                                                       language,
                                                                                                       files_from_at)
    if at_df is not None and does_contain_ct_name:
        at_id = get_parent_folder_name(at_file).split('_')[1]
        ct_df = ath.merge_code_tracker_and_activity_tracker_data(ct_df, at_df, at_id)
        return ct_df

    at_new_data = pd.DataFrame(ath.get_full_default_columns_for_at(ct_df.shape[0]))
    ct_df = ct_df.join(at_new_data)
    return ct_df


def preprocess_data(path):
    result_folder = get_result_folder(path, consts.PREPROCESSING_RESULT_FOLDER)
    folders = get_all_file_system_items(path, data_subdirs_condition, consts.FILE_SYSTEM_ITEM.SUBDIR.value)
    for folder in folders:
        log.info('Start handling the folder ' + folder)
        files = get_all_file_system_items(folder, csv_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
        try:
            ct_files, at_file = __separate_at_and_other_files(files)
        # Drop the current folder
        except ValueError:
            continue

        at_df = handle_at_file(at_file)

        for ct_file in ct_files:
            ct_df, language = handle_ct_file(ct_file)
            ct_df = handle_ct_and_at(ct_file, ct_df, at_file, at_df, language)

            write_result(result_folder, path, ct_file, ct_df)

        log.info('Finish handling the folder ' + folder)
    return result_folder
