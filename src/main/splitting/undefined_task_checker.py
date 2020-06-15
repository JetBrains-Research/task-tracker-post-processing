# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import sys
import logging
from typing import List

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.splitting.task_checker import ITaskChecker, SOURCE_OBJECT_NAME, FilesDict

log = logging.getLogger(consts.LOGGER_NAME)


class UndefinedTaskChecker(ITaskChecker):

    @property
    def language(self) -> LANGUAGE:
        return LANGUAGE.UNDEFINED

    @property
    def min_symbols_number(self) -> int:
        return sys.maxsize

    @property
    def output_strings(self) -> List[str]:
        return []

    def create_source_file(self, source_code: str) -> str:
        return self.create_source_file_with_name(source_code, SOURCE_OBJECT_NAME)

    def is_source_file_correct(self, source_file: str) -> bool:
        return False

    def run_test(self, input: str, expected_output: str, source_file: str) -> bool:
        return False

    def check_tasks(self, tasks: list, source_code: str, in_and_out_files_dict: FilesDict,
                    stop_after_first_false: bool = True) -> List[int]:
        rate = consts.TEST_RESULT.INCORRECT_CODE.value
        return [rate] * len(tasks)
