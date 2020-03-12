# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import re
import logging

import pandas as pd

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.splitting.task_checker import TASKS_TESTS_PATH
from src.main.splitting.cpp_task_checker import CppTaskChecker
from src.main.splitting.java_task_checker import JavaTaskChecker
from src.main.splitting.kotlin_task_checker import KotlinTaskChecker
from src.main.splitting.python_task_checker import PythonTaskChecker
from src.main.preprocessing.code_tracker_handler import get_ct_language
from src.main.splitting.not_defined_task_checker import NotDefinedTaskChecker
from src.main.util.file_util import get_all_file_system_items, get_parent_folder_name, get_name_from_path, \
    ct_file_condition, get_result_folder, write_based_on_language, get_file_and_parent_folder_names, \
    pair_in_and_out_files

log = logging.getLogger(consts.LOGGER_NAME)

FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value
TESTS_RESULTS = consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value


def create_in_and_out_dict(tasks: list):
    in_and_out_files_dict = {}
    for task in tasks:
        root = os.path.join(TASKS_TESTS_PATH, task)
        in_files = get_all_file_system_items(root, (lambda filename: re.fullmatch(r'in_\d+.txt', filename)))
        out_files = get_all_file_system_items(root, (lambda filename: re.fullmatch(r'out_\d+.txt', filename)))
        if len(out_files) != len(in_files):
            raise ValueError('Length of out files list does not equal in files list')
        in_and_out_files_dict[task] = pair_in_and_out_files(in_files, out_files)
    return in_and_out_files_dict


def check_tasks(tasks: list, source_code: str, in_and_out_files_dict: dict, language=LANGUAGE.PYTHON.value, stop_after_first_false=True):
    if language == LANGUAGE.PYTHON.value:
        task_checker = PythonTaskChecker()
    elif language == LANGUAGE.JAVA.value:
        task_checker = JavaTaskChecker()
    elif language == LANGUAGE.CPP.value:
        task_checker = CppTaskChecker()
    elif language == LANGUAGE.KOTLIN.value:
        task_checker = KotlinTaskChecker()
    else:
        task_checker = NotDefinedTaskChecker()

    return task_checker.check_tasks(tasks, source_code, in_and_out_files_dict, stop_after_first_false)


def __check_tasks_on_correct_fragments(data: pd.DataFrame, tasks: list, in_and_out_files_dict: dict, file_log_info=''):
    data[FRAGMENT] = data[FRAGMENT].fillna('')
    # if run after preprocessing, this value can be taken from 'language' column
    language = get_ct_language(data)
    log.info(f'{file_log_info}, language is {language}, found {str(data.shape[0])} fragments')

    if language is consts.LANGUAGE.NOT_DEFINED.value:
        data[TESTS_RESULTS] = str([consts.TEST_RESULT.LANGUAGE_NOT_DEFINED.value] * len(tasks))
    else:
        unique_fragments = list(data[FRAGMENT].unique())
        log.info(f'Found {str(len(unique_fragments))} unique fragments')

        fragment_to_test_results_dict = dict(
            map(lambda f: (f, check_tasks(tasks, f, in_and_out_files_dict, language)), unique_fragments))
        data[TESTS_RESULTS] = data.apply(lambda row: fragment_to_test_results_dict[row[FRAGMENT]], axis=1)

    return language, data


def filter_already_tested_files(files: list, result_folder_path: str):
    tested_files = get_all_file_system_items(result_folder_path, ct_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    tested_folder_and_file_names = list(map(lambda f: get_file_and_parent_folder_names(f), tested_files))
    return list(filter(lambda f: get_file_and_parent_folder_names(f) not in tested_folder_and_file_names, files))


def run_tests(path: str):
    log.info(f'Start running tests on path {path}')
    result_folder = get_result_folder(path, consts.RUNNING_TESTS_RESULT_FOLDER)

    files = get_all_file_system_items(path, ct_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    str_len_files = str(len(files))
    log.info(f'Found {str_len_files} files to run tests on them')

    files = filter_already_tested_files(files, result_folder)
    str_len_files = str(len(files))
    log.info(f'Found {str_len_files} files to run tests on them after filtering already tested')

    tasks = [t.value for t in consts.TASK]
    in_and_out_files_dict = create_in_and_out_dict(tasks)

    for i, file in enumerate(files):
        file_log_info = f'file: {str(i + 1)}/{str_len_files}'
        log.info(f'Start running tests on {file_log_info}, {file}')
        data = pd.read_csv(file, encoding=consts.ISO_ENCODING)
        language, data = __check_tasks_on_correct_fragments(data, tasks, in_and_out_files_dict, file_log_info)
        log.info(f'Finish running tests on {file_log_info}, {file}')
        write_based_on_language(result_folder, file, data, language)

    return result_folder
