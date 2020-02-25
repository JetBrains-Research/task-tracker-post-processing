import os
import sys
import logging

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.util.file_util import create_file
from src.main.util.language_util import get_extension_by_language
from src.main.splitting.task_checker import ITaskChecker, TASKS_TESTS_PATH, SOURCE_OBJECT_NAME


log = logging.getLogger(consts.LOGGER_NAME)


class NotDefinedTaskChecker(ITaskChecker):

    @property
    def language(self):
        return LANGUAGE.NOT_DEFINED.value

    @property
    def min_symbols_number(self):
        return sys.maxsize

    @property
    def output_strings(self):
        return []

    def create_source_file(self, source_code: str):
        source_code_file = os.path.join(TASKS_TESTS_PATH, SOURCE_OBJECT_NAME,
                                        SOURCE_OBJECT_NAME + get_extension_by_language(self.language))
        create_file(source_code, source_code_file)
        return source_code_file

    def is_source_file_correct(self, source_file: str):
        return False

    def run_test(self, input: str, expected_output: str, source_file: str):
        return False

    def check_tasks(self, tasks: list, source_code: str, in_and_out_files_dict: dict, stop_after_first_false=True):
        rate = consts.TEST_RESULT.INCORRECT_CODE.value
        return [rate] * len(tasks)
