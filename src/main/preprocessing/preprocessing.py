import csv
import logging
import os
from os import makedirs

import pandas as pd

from src.main.preprocessing.activity_tracker_handler import handle_at_file, get_ct_name_from_at_data, \
    get_files_from_at
from src.main.preprocessing.code_tracker_handler import handle_ct_file
from src.main.preprocessing import activity_tracker_handler as ath
from src.main.util import consts
from src.main.util.file_util import create_directory, get_all_file_system_items, data_subdirs_condition, \
    csv_file_condition, get_parent_folder, get_parent_folder_name, get_file_name_from_path

log = logging.getLogger(consts.LOGGER_NAME)


# Write result next to the passed path to not disorder the passed data folder
# The name of result folder contains the passed data folder name
def __write_result(path: str, file: str, result_df: pd.DataFrame):
    path_folder_name = get_file_name_from_path(path)
    result_folder_name = path_folder_name + "_" + consts.PREPROCESSING_RESULT_FOLDER
    path_from_result_folder_to_file = file[len(path):]

    file_to_write = os.path.join(get_parent_folder(path), result_folder_name, path_from_result_folder_to_file)
    folder_to_write = get_parent_folder(file_to_write)

    if not os.path.exists(folder_to_write):
        makedirs(folder_to_write)

    # get error with this encoding=ENCODING on ati_225/153e12:
    # "UnicodeEncodeError: 'latin-1' codec can't encode character '\u0435' in position 36: ordinal not in range(256)"
    # So change it then to 'utf-8'
    try:
        result_df.to_csv(file_to_write, encoding=consts.ENCODING, index=False)
    except UnicodeEncodeError:
        result_df.to_csv(file_to_write, encoding='utf8', index=False)


def __get_real_at_file_index(files: list):
    sniffer = csv.Sniffer()
    sample_bytes = 1024
    count_at = 0
    at_index = -1
    for i, f in enumerate(files):
        if consts.ACTIVITY_TRACKER_FILE_NAME in f:
            if not sniffer.has_header(open(f, encoding=consts.ENCODING).read(sample_bytes)):
                count_at += 1
                at_index = i
                if count_at >= 2:
                    raise ValueError('Count of activity tracker files is more 1')
    return at_index


def __separate_at_and_other_files(files: list):
    at_file_index = __get_real_at_file_index(files)
    at_file = None
    if at_file_index != -1:
        at_file = files[at_file_index]
        del files[at_file_index]
    return files, at_file


def handle_ct_and_at(ct_file, ct_df, at_file, at_df, language):
    if at_df is not None:
        files_from_at = get_files_from_at(at_df)
        ct_df[consts.CODE_TRACKER_COLUMN.FILE_NAME.value], does_contain_ct_name = get_ct_name_from_at_data(ct_file,
                                                                                                           language,
                                                                                                           files_from_at)
        if does_contain_ct_name:
            at_id = get_parent_folder_name(at_file).split('_')[1]
            ct_df = ath.merge_code_tracker_and_activity_tracker_data(ct_df, at_df, at_id)
            return ct_df

    at_new_data = pd.DataFrame(ath.get_full_default_columns_for_at(ct_df.shape[0]))
    ct_df = ct_df.join(at_new_data)
    return ct_df


def preprocess_data(path):
    folders = get_all_file_system_items(path, data_subdirs_condition, consts.FILE_SYSTEM_ITEM.SUBDIR.value)

    for folder in folders:
        log.info('Start handling the folder ' + folder)
        files = get_all_file_system_items(folder, csv_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
        ct_files, at_file = __separate_at_and_other_files(files)

        at_df = handle_at_file(at_file)

        for ct_file in ct_files:
            ct_df, language = handle_ct_file(ct_file)
            ct_df = handle_ct_and_at(ct_file, ct_df, at_file, at_df, language)

            # look into
            __write_result(path, ct_file, ct_df)

        log.info('Finish handling the folder ' + folder)
