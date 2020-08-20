# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import re
import logging
from typing import List, Dict, Tuple, Optional

import pandas as pd

from src.main.util import consts
from src.main.util.consts import LANGUAGE, TASK
from src.main.util.log_util import log_and_raise_error
from src.main.splitting.cpp_task_checker import CppTaskChecker
from src.main.splitting.java_task_checker import JavaTaskChecker
from src.main.splitting.kotlin_task_checker import KotlinTaskChecker
from src.main.splitting.python_task_checker import PythonTaskChecker
from src.main.preprocessing.code_tracker_handler import get_ct_language
from src.main.splitting.task_checker import TASKS_TESTS_PATH, FilesDict
from src.main.splitting.undefined_task_checker import UndefinedTaskChecker
from src.main.util.file_util import get_all_file_system_items, ct_file_condition, get_output_directory, \
    write_based_on_language, get_file_and_parent_folder_names, pair_in_and_out_files, match_condition, \
    get_name_from_path, get_original_file_name

log = logging.getLogger(consts.LOGGER_NAME)

FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value
TESTS_RESULTS = consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value


def create_in_and_out_dict(tasks: List[TASK]) -> FilesDict:
    in_and_out_files_dict = {}
    for task in tasks:
        root = os.path.join(TASKS_TESTS_PATH, task.value)
        in_files = get_all_file_system_items(root, match_condition(r'in_\d+.txt'))
        out_files = get_all_file_system_items(root, match_condition(r'out_\d+.txt'))
        if len(out_files) != len(in_files):
            log_and_raise_error('Length of out files list does not equal in files list', log)
        in_and_out_files_dict[task] = pair_in_and_out_files(in_files, out_files)
    return in_and_out_files_dict


def check_tasks(tasks: List[TASK], source_code: str, in_and_out_files_dict: FilesDict,
                language: LANGUAGE = LANGUAGE.PYTHON, stop_after_first_false: bool = True,
                current_task: Optional[TASK] = None) -> List[float]:
    if language == LANGUAGE.PYTHON:
        task_checker = PythonTaskChecker()
    elif language == LANGUAGE.JAVA:
        task_checker = JavaTaskChecker()
    elif language == LANGUAGE.CPP:
        task_checker = CppTaskChecker()
    elif language == LANGUAGE.KOTLIN:
        task_checker = KotlinTaskChecker()
    else:
        task_checker = UndefinedTaskChecker()

    return task_checker.check_tasks(tasks, source_code, in_and_out_files_dict, stop_after_first_false,
                                    current_task=current_task)


def __check_tasks_on_correct_fragments(data: pd.DataFrame, tasks: List[TASK], in_and_out_files_dict: FilesDict,
                                       file_log_info: str = '',
                                       current_task: Optional[TASK] = None) -> Tuple[LANGUAGE, pd.DataFrame]:
    data[FRAGMENT] = data[FRAGMENT].fillna('')
    # If run after preprocessing, this value can be taken from 'language' column
    language = get_ct_language(data)
    log.info(f'{file_log_info}, language is {language.value}, found {str(data.shape[0])} fragments')

    if language == consts.LANGUAGE.UNDEFINED:
        data[TESTS_RESULTS] = str([consts.TEST_RESULT.LANGUAGE_UNDEFINED.value] * len(tasks))
    else:
        unique_fragments = list(data[FRAGMENT].unique())
        log.info(f'Found {str(len(unique_fragments))} unique fragments')

        fragment_to_test_results_dict = dict(
            map(lambda f:
                (f, check_tasks(tasks, f, in_and_out_files_dict, language, current_task=current_task)),
                unique_fragments))
        data[TESTS_RESULTS] = data.apply(lambda row: fragment_to_test_results_dict[row[FRAGMENT]], axis=1)

    return language, data


def filter_already_tested_files(files: List[str], output_directory_path: str) -> List[str]:
    tested_files = get_all_file_system_items(output_directory_path, ct_file_condition)
    tested_folder_and_file_names = list(map(lambda f: get_file_and_parent_folder_names(f), tested_files))
    return list(filter(lambda f: get_file_and_parent_folder_names(f) not in tested_folder_and_file_names, files))


def __get_task_by_ct_file(file: str) -> Optional[TASK]:
    file_name = get_name_from_path(file, with_extension=False)
    task_key = get_original_file_name(file_name)
    try:
        return TASK(task_key)
    except ValueError:
        log.info(f'Unexpected task for the file {file}')
        return None


def run_tests(path: str) -> str:
    log.info(f'Start running tests on path {path}')
    output_directory = get_output_directory(path, consts.RUNNING_TESTS_OUTPUT_DIRECTORY)

    files = get_all_file_system_items(path, ct_file_condition)
    str_len_files = str(len(files))
    log.info(f'Found {str_len_files} files to run tests on them')

    files = filter_already_tested_files(files, output_directory)
    str_len_files = str(len(files))
    log.info(f'Found {str_len_files} files to run tests on them after filtering already tested')

    tasks = TASK.tasks()
    in_and_out_files_dict = create_in_and_out_dict(tasks)

    for i, file in enumerate(files):
        file_log_info = f'file: {str(i + 1)}/{str_len_files}'
        log.info(f'Start running tests on {file_log_info}, {file}')
        current_task = __get_task_by_ct_file(file)
        data = pd.read_csv(file, encoding=consts.ISO_ENCODING)
        language, data = __check_tasks_on_correct_fragments(data, tasks, in_and_out_files_dict, file_log_info,
                                                            current_task=current_task)
        log.info(f'Finish running tests on {file_log_info}, {file}')
        write_based_on_language(output_directory, file, data, language)

    return output_directory


print(run_tests('/Users/Anastasiia.Birillo/PycharmProjects/codetracker-data/data_1/dataset'))