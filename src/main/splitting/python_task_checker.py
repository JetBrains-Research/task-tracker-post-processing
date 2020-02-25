import os
import sys
import logging

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.util.file_util import create_file
from src.main.util.language_util import get_extension_by_language
from src.main.splitting.task_checker import ITaskChecker, check_call_safely, check_output_safely, TASKS_TESTS_PATH, \
    SOURCE_OBJECT_NAME

log = logging.getLogger(consts.LOGGER_NAME)


class PythonTaskChecker(ITaskChecker):

    @property
    def language(self):
        return LANGUAGE.PYTHON.value

    # a=int(input())
    # print(a)
    @property
    def min_symbols_number(self):
        return 20

    @property
    def output_strings(self):
        return ['print']

    def create_source_file(self, source_code: str):
        source_code_file = os.path.join(TASKS_TESTS_PATH, SOURCE_OBJECT_NAME,
                                        SOURCE_OBJECT_NAME + get_extension_by_language(self.language))
        create_file(source_code, source_code_file)
        return source_code_file

    def is_source_file_correct(self, source_file: str):
        is_correct = check_call_safely(['mypy', source_file]) and check_call_safely([sys.executable, source_file])
        log.info(f'Source code is correct: {is_correct}')
        return is_correct

    def run_test(self, input: str, expected_output: str, source_file: str):
        args = [sys.executable, source_file]
        return check_output_safely(input, expected_output, args)
