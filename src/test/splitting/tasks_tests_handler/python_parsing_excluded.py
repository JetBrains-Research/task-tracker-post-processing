# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import sys
import logging
from subprocess import check_output, CalledProcessError

from src.main.util import consts
from src.test.test_util import LoggedTest
from src.main.util.consts import TEST_DATA_PATH
from src.main.splitting.task_checker import check_call_safely
from src.main.util.file_util import get_all_file_system_items, extension_file_condition

"""
EXCLUDED
These tests aren't included in all tests running because it's unnecessary to compare pylint and mypy again.
We have already chosen mypy.
"""

log = logging.getLogger(consts.LOGGER_NAME)

PARSING_TEST_DATA_PATH = os.path.join(TEST_DATA_PATH, "splitting/tasks_tests_handler/python_parsing/")


def check_python_file_by_mypy(file_name: str) -> bool:
    call_args = ['mypy', file_name]
    return check_call_safely(call_args)


def check_python_file_by_pylint(file_name: str) -> bool:
    call_args = ['pylint', '-E', file_name]
    try:
        actual_out = check_output(call_args, universal_newlines=True)
        return 'E:' not in actual_out
    except CalledProcessError:
        return False


def check_file_by_mypy_and_execution(file_name: str) -> bool:
    return check_call_safely(['mypy', file_name]) and check_call_safely([sys.executable, file_name])


class TestPythonParsing(LoggedTest):

   def test_python_parsing(self) -> None:
        log.info('mypy and pylint testing:')
        # Files contain 12 incorrect files, which have 'error' in their names, and 1 correct file, which hasn't
        files = get_all_file_system_items(PARSING_TEST_DATA_PATH, extension_file_condition(consts.EXTENSION.TXT))
        mypy_rate = 0
        pylint_rate = 0
        mypy_with_execution_rate = 0
        for file in files:
            log.info(file)

            mypy = check_python_file_by_mypy(file)
            mypy_rate += ('error' in file) != mypy

            pylint = check_python_file_by_pylint(file)
            pylint_rate += ('error' in file) != pylint

            mypy_with_execution = check_file_by_mypy_and_execution(file)
            mypy_with_execution_rate += ('error' in file) != mypy_with_execution

            log.info(f'mypy: {mypy}, pylint: {pylint}, mypy with compile: {mypy_with_execution}')

        log.info(f'mypy: {mypy_rate}, pylint: {pylint_rate}, mypy with compile: {mypy_with_execution_rate}, all: {len(files)}')
