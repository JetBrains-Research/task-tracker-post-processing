import os
import logging
from os import makedirs

import numpy as np
import pandas as pd

from src.main.util import consts
from src.main.preprocessing.code_tracker_handler import get_ct_language
from src.main.splitting.tasks_tests_handler import check_tasks, create_in_and_out_dict
from src.main.util.file_util import ct_file_condition, get_all_file_system_items, get_file_name_from_path, \
    get_parent_folder, get_parent_folder_name, get_result_folder, write_based_on_language

FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value

log = logging.getLogger(consts.LOGGER_NAME)


def get_tasks_with_max_rate(tasks: list, test_results: list):
    max_rate = max(test_results)
    indices = [i for i, tr in enumerate(test_results) if tr == max_rate]
    return [tasks[i] for i in indices], max_rate


def check_tasks_on_fragment_and_add_to_dict(fragment, dict, tasks, in_and_out_files_dict, language):
    print("hey")
    # dict[fragment] = check_tasks(tasks, fragment, in_and_out_files_dict, language)


def check_tasks_on_correct_fragments(data: pd.DataFrame, tasks: list, in_and_out_files_dict: dict, file_log_info=""):
    data[FRAGMENT] = data[FRAGMENT].fillna("")
    # if run after preprocessing, this value can be taken from 'language' column
    language = get_ct_language(data)
    # add unique to logs
    log.info(file_log_info + ", language is " + language + ", found " + str(data.shape[0]) + " fragments")

    if language is not consts.LANGUAGE.NOT_DEFINED.value:
        unique_fragments = list(data[FRAGMENT].unique())
        log.info("Found " + str(len(unique_fragments)) + " unique fragments")

        fragment_to_test_results_dict = dict(map(lambda f: (f, check_tasks(tasks, f, in_and_out_files_dict, language)), unique_fragments))
        data[consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value] = data.apply(lambda row:
                                                                          fragment_to_test_results_dict[row[FRAGMENT]], axis=1)
    else:
        data[consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value] = str([consts.TEST_RESULT.LANGUAGE_NOT_DEFINED.value] * len(tasks))

    return language, data


# since lists of tasks have small size, it should work faster than creating a set
def intersect(list_1: list, list_2: list):
    return [e for e in list_1 if e in list_2]


# first version of splitting
def find_real_splits(supposed_splits: list):
    real_splits = []
    if len(supposed_splits) == 0:
        return real_splits

    prev_split = supposed_splits[0]
    prev_intersected_tasks = prev_split[consts.SPLIT_DICT.TASKS.value]

    for curr_split in supposed_splits:
        curr_intersected_tasks = intersect(prev_intersected_tasks, curr_split[consts.SPLIT_DICT.TASKS.value])
        if len(curr_intersected_tasks) == 0:
            # it means that the supposed task has changed, so we should split on prev_split
            real_splits.append({consts.SPLIT_DICT.INDEX.value: prev_split[consts.SPLIT_DICT.INDEX.value],
                                consts.SPLIT_DICT.RATE.value: prev_split[consts.SPLIT_DICT.RATE.value],
                                consts.SPLIT_DICT.TASKS.value: prev_intersected_tasks})
            prev_intersected_tasks = curr_split[consts.SPLIT_DICT.TASKS.value]
        else:
            prev_intersected_tasks = curr_intersected_tasks

        prev_split = curr_split

    # add the last split
    real_splits.append({consts.SPLIT_DICT.INDEX.value: prev_split[consts.SPLIT_DICT.INDEX.value],
                        consts.SPLIT_DICT.RATE.value: prev_split[consts.SPLIT_DICT.RATE.value],
                        consts.SPLIT_DICT.TASKS.value: prev_intersected_tasks})
    return real_splits


def filter_already_tested_files(files, result_folder_path):
    tested_files = get_all_file_system_items(result_folder_path, ct_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    # to get something like 'ati_239/Main_2323434_343434.csv'
    tested_folder_and_file_names = list(map(lambda f: get_parent_folder_name(f) + "/" + get_file_name_from_path(f), tested_files))
    return list(filter(lambda f: get_parent_folder_name(f) + "/" + get_file_name_from_path(f) not in tested_folder_and_file_names, files))


def run_tests(path: str):
    log.info("Start running tests on path " + path)
    result_folder = get_result_folder(path, consts.RUNNING_TESTS_RESULT_FOLDER)

    files = get_all_file_system_items(path, ct_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    str_len_files = str(len(files))
    log.info("Found " + str_len_files + " files to run tests on them")

    files = filter_already_tested_files(files, result_folder)
    str_len_files = str(len(files))
    log.info("Found " + str_len_files + " files to run tests on them after filtering already tested")

    tasks = [t.value for t in consts.TASK]
    in_and_out_files_dict = create_in_and_out_dict(tasks)

    for i, file in enumerate(files):
        file_log_info = "file: " + str(i + 1) + "/" + str_len_files
        log.info("Start running tests on " + file_log_info + ", " + file)
        data = pd.read_csv(file, encoding=consts.ENCODING)
        language, data = check_tasks_on_correct_fragments(data, tasks, in_and_out_files_dict, file_log_info)
        log.info("Finish running tests on " + file_log_info + ", " + file)
        write_based_on_language(result_folder, file, data, language)

    return result_folder
