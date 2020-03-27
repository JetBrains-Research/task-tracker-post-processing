# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import re
import logging

from enum import Enum
from typing import Callable

from src.main.util.consts import LOGGER_NAME, ROOT_DIR
from src.main.util.file_util import get_all_file_system_items, pair_in_and_out_files, get_content_from_file

log = logging.getLogger(LOGGER_NAME)


class CANONIZATION_TESTS(Enum):
    TASKS_TESTS_PATH = ROOT_DIR + '/../../resources'
    INPUT_FILE_NAME = 'in'
    OUTPUT_FILE_NAME = 'out'


class CANONIZATION_TESTS_TYPES(Enum):
    CLEANED_CODE = 'cleaned_code'
    ANONYMIZE_NAMES = 'anonymize_names'
    CANONICAL_FORM = 'canonical_form'
    STUDENT_CODE = 'student_code'


def get_test_in_and_out_files(test_type: CANONIZATION_TESTS_TYPES, task=None) -> list:
    root = os.path.join(CANONIZATION_TESTS.TASKS_TESTS_PATH.value, str(test_type))
    if task is not None:
        root = os.path.join(root, str(task))
    in_files = get_all_file_system_items(root, (lambda filename: re.fullmatch(r'in_\d+.py', filename)))
    out_files = get_all_file_system_items(root, (lambda filename: re.fullmatch(r'out_\d+.py', filename)))
    if len(out_files) != len(in_files):
        raise ValueError('Length of out files list does not equal in files list')
    return pair_in_and_out_files(in_files, out_files)


def run_test(self, test_type: CANONIZATION_TESTS_TYPES, get_code: Callable, task=None) -> None:
    files = get_test_in_and_out_files(test_type, task)
    count_tests = 1
    for source_code, expected_code_path in files:
        log.info(f'Test number is {count_tests}\nSource code is: {source_code}\n')
        actual_code = get_code(source_code)
        expected_code = get_content_from_file(expected_code_path)
        log.info(f'Actual code is:\n{actual_code}\nExpected code is:\n{expected_code}\n')
        self.assertEqual(expected_code, actual_code)
        count_tests += 1
