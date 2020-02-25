# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import re
import logging

from typing import Callable

from src.main.util.consts import LOGGER_NAME, CANONIZATION_TESTS, CANONIZATION_TESTS_TYPES
from src.main.util.file_util import get_all_file_system_items, pair_in_and_out_files, get_content_from_file

log = logging.getLogger(LOGGER_NAME)


def get_test_in_and_out_files(test_type: CANONIZATION_TESTS_TYPES):
    root = os.path.join(CANONIZATION_TESTS.TASKS_TESTS_PATH.value, str(test_type))
    in_files = get_all_file_system_items(root, (lambda filename: re.fullmatch(r'in_\d+.py', filename)))
    out_files = get_all_file_system_items(root, (lambda filename: re.fullmatch(r'out_\d+.py', filename)))
    if len(out_files) != len(in_files):
        raise ValueError('Length of out files list does not equal in files list')
    return pair_in_and_out_files(in_files, out_files)


def run_test(self, test_type: CANONIZATION_TESTS_TYPES, get_code: Callable):
    files = get_test_in_and_out_files(test_type)
    count_tests = 1
    for source_code, expected_code_path in files:
        actual_code = get_code(source_code)
        expected_code = get_content_from_file(expected_code_path)
        log.info(f'Test number is {count_tests}\nActual code is:\n{actual_code}\nExpected code '
                 f'is:\n{expected_code}\n')
        self.assertEqual(expected_code, actual_code)
        count_tests += 1
