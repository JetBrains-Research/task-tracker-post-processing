# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import List, Tuple

import pandas as pd

from src.main.util import consts
from src.main.util.consts import EXTENSION
from src.main.util.file_util import get_output_directory, get_all_file_system_items, data_subdirs_condition, \
    all_items_condition, extension_file_condition, sort_files_by_size

log = logging.getLogger(consts.LOGGER_NAME)


def __get_ct_and_ati_files(files: List[str]) -> Tuple[List[str], List[str]]:
    ati_files = [f for f in files if 'ide_events' in f]
    ct_files = [f for f in files if f not in ati_files]
    return ct_files, ati_files


def __merge_ati_files(ati_files: List[str]) -> pd.DataFrame:
    ati_df = pd.DataFrame(columns=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    for ati_file in ati_files:
        current_ati_df = pd.read_csv(ati_file, encoding=consts.ISO_ENCODING,
                                     names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
        ati_df.append(current_ati_df, ignore_index=True)
    ati_df.drop_duplicates(keep='first')
    return ati_df


def prepare_data_for_preprocessing(path: str) -> str:
    output_directory = get_output_directory(path, consts.TEST_MODE_REMOVING_DIRECTORY)
    user_folders = get_all_file_system_items(path, lambda dir: 'user' in dir, consts.FILE_SYSTEM_ITEM.SUBDIR)
    for user_folder in user_folders:
        log.info(f'Start handling the folder {user_folder}')
        task_folders = get_all_file_system_items(path, all_items_condition, consts.FILE_SYSTEM_ITEM.SUBDIR)
        for task_folder in task_folders:
            files = get_all_file_system_items(path, extension_file_condition(EXTENSION.CSV))
            ct_files, ati_files = __get_ct_and_ati_files(files)
            pass
    pass


def delete_duplicates(ct_files: List[str]) -> str:
    if not ct_files:
        pass
    if len(ct_files) == 1:
        return ct_files[0]
    import os
    ct_files.sort(key=lambda f: os.stat(f).st_size, reverse=True)
    print(ct_files)

    pass