# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

from src.main.util import consts
from src.main.preprocessing.preprocessing import is_ct_file
from src.main.util.consts import FILE_SYSTEM_ITEM, LOGGER_NAME
from src.main.util.file_util import get_all_file_system_items, get_file_and_parent_folder_names, create_file, \
    get_content_from_file, ct_file_condition, csv_file_condition

log = logging.getLogger(LOGGER_NAME)


# To find all '.csv' files in root with the same names as in result folder and replace them
def replace_ct_files(path: str, tested_path: str):
    files = get_all_file_system_items(path, csv_file_condition, FILE_SYSTEM_ITEM.FILE.value)
    tested_files = get_all_file_system_items(tested_path, csv_file_condition, FILE_SYSTEM_ITEM.FILE.value)

    # Just for checking
    folder_and_file_names = set(map(lambda f: get_file_and_parent_folder_names(f), files))
    tested_folder_and_file_names = set(map(lambda f: get_file_and_parent_folder_names(f), tested_files))
    log.info(f'Symmetric difference between tested and not files is {folder_and_file_names.symmetric_difference(tested_folder_and_file_names)}')

    for file in files:
        filtered_tested_files = list(filter(lambda f: get_file_and_parent_folder_names(file) == get_file_and_parent_folder_names(f), tested_files))
        if len(filtered_tested_files) == 0:
            log.info(f'There is no tested_file for {file}')
        elif len(filtered_tested_files) == 1:
            tested_file = filtered_tested_files[0]
            log.info(f'Found one tested file for {file}, it is {tested_file}')
            content = get_content_from_file(tested_file)
            create_file(content, file)
        else:
            log.error(f'Found several files for {file}, they are {tested_files}')
            raise ValueError(f'Found several files for {file}, they are {tested_files}')


def check_replacing(path: str):
    ct_files = get_all_file_system_items(path, ct_file_condition, FILE_SYSTEM_ITEM.FILE.value)
    not_ct_files = list(filter(lambda f: not is_ct_file(f, consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value), ct_files))
    if not_ct_files:
        log.error(f'Some of ct files does not have \'testsResults\' column: {not_ct_files}')
        raise ValueError(f'Some of ct files does not have \'testsResults\' column: {not_ct_files}')
