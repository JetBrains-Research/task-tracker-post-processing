import os
import logging
from os import makedirs

import pandas as pd

from main.splitting.tasks_tests_handler import check_tasks, create_in_and_out_dict
from src.main.preprocessing.code_tracker_handler import get_ct_language
from src.main.util import consts
from src.main.util.consts import ENCODING, CODE_TRACKER_COLUMN, LANGUAGE, TASK, \
    FILE_SYSTEM_ITEM, SPLIT_DICT
from src.main.util.file_util import ct_file_condition, get_all_file_system_items, get_file_name_from_path, \
    get_parent_folder, get_parent_folder_name

FRAGMENT = CODE_TRACKER_COLUMN.FRAGMENT.value

log = logging.getLogger(consts.LOGGER_NAME)


def get_tasks_with_max_rate(tasks: list, test_results: list):
    max_rate = max(test_results)
    indices = [i for i, tr in enumerate(test_results) if tr == max_rate]
    return [tasks[i] for i in indices], max_rate


def check_tasks_on_correct_fragments(data: pd.DataFrame, tasks: list, in_and_out_files_dict: dict, file_log_info: str):
    data[FRAGMENT] = data[FRAGMENT].fillna("")
    # if run after preprocessing, this value can be taken from 'language' column
    language = get_ct_language(data)
    log.info(file_log_info + ", language is " + language + ", found " + str(data.shape[0]) + " fragments")
    if language is not LANGUAGE.NOT_DEFINED.value:
        data[CODE_TRACKER_COLUMN.TESTS_RESULTS.value] = data.apply(lambda row:
                                                                   check_tasks(tasks, row[FRAGMENT],
                                                                               in_and_out_files_dict, language),
                                                                   axis=1)
    else:
        data[CODE_TRACKER_COLUMN.TESTS_RESULTS.value] = [consts.TEST_RESULT.LANGUAGE_NOT_DEFINED.value] * len(tasks)

    return language, data


# since lists of tasks have small size, it should work faster than creating a set
def intersect(list_1: list, list_2: list):
    return [e for e in list_1 if e in list_2]


def find_real_splits(supposed_splits: list):
    real_splits = []
    if len(supposed_splits) == 0:
        return real_splits

    prev_split = supposed_splits[0]
    prev_intersected_tasks = prev_split[SPLIT_DICT.TASKS.value]

    for curr_split in supposed_splits:
        curr_intersected_tasks = intersect(prev_intersected_tasks, curr_split[SPLIT_DICT.TASKS.value])
        if len(curr_intersected_tasks) == 0:
            # it means that the supposed task has changed, so we should split on prev_split
            real_splits.append({SPLIT_DICT.INDEX.value: prev_split[SPLIT_DICT.INDEX.value],
                                SPLIT_DICT.RATE.value: prev_split[SPLIT_DICT.RATE.value],
                                SPLIT_DICT.TASKS.value: prev_intersected_tasks})
            prev_intersected_tasks = curr_split[SPLIT_DICT.TASKS.value]
        else:
            prev_intersected_tasks = curr_intersected_tasks

        prev_split = curr_split

    # add the last split
    real_splits.append({SPLIT_DICT.INDEX.value: prev_split[SPLIT_DICT.INDEX.value],
                        SPLIT_DICT.RATE.value: prev_split[SPLIT_DICT.RATE.value],
                        SPLIT_DICT.TASKS.value: prev_intersected_tasks})
    return real_splits


def write_based_on_language(path, file, data, language):
    result_folder_name = get_file_name_from_path(path) + "_" + consts.RUNNING_TESTS_RESULT_FOLDER
    folder_to_write = os.path.join(get_parent_folder(path), result_folder_name, language, get_parent_folder_name(file))
    file_to_write = os.path.join(folder_to_write, get_file_name_from_path(file))

    if not os.path.exists(folder_to_write):
        makedirs(folder_to_write)

    log.info("Write file: " + file + " to: " + file_to_write)
    try:
        data.to_csv(file_to_write, encoding=consts.ENCODING, index=False)
    except UnicodeEncodeError:
        data.to_csv(file_to_write, encoding='utf8', index=False)


def run_tests(path: str):
    log.info("Start running tests on path " + path)
    files = get_all_file_system_items(path, ct_file_condition, FILE_SYSTEM_ITEM.FILE.value)
    str_len_files = str(len(files))
    log.info("Found " + str_len_files + " files to run tests on them")
    tasks = [t.value for t in TASK]
    in_and_out_files_dict = create_in_and_out_dict(tasks)

    for i, file in enumerate(files):
        file_log_info = "file: " + str(i + 1) + "/" + str_len_files
        log.info("Start running tests on " + file_log_info + ", " + file)
        data = pd.read_csv(file, encoding=ENCODING)
        language, data = check_tasks_on_correct_fragments(data, tasks, in_and_out_files_dict, file_log_info)
        log.info("Finish running tests on " + file_log_info + ", " + file)
        write_based_on_language(path, file, data, language)