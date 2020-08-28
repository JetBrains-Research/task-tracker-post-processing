# Copyright (c) by anonymous author(s)

import sys
import logging
from typing import List

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.splitting.task_checker import ITaskChecker, check_call_safely, check_output_safely, SOURCE_OBJECT_NAME

log = logging.getLogger(consts.LOGGER_NAME)


class PythonTaskChecker(ITaskChecker):

    @property
    def language(self) -> LANGUAGE:
        return LANGUAGE.PYTHON

    # a=int(input())
    # print(a)
    @property
    def min_symbols_number(self) -> int:
        return 20

    @property
    def output_strings(self) -> List[str]:
        return ['print']

    def create_source_file(self, source_code: str) -> str:
        return self.create_source_file_with_name(source_code, SOURCE_OBJECT_NAME)

    def is_source_file_correct(self, source_file: str) -> bool:
        is_correct = check_call_safely(['mypy', source_file]) and check_call_safely([sys.executable, source_file],
                                                                                    shell=True)
        log.info(f'Source code is correct: {is_correct}')
        return is_correct

    def run_test(self, input: str, expected_output: str, source_file: str) -> bool:
        args = [sys.executable, source_file]
        return check_output_safely(input, expected_output, args)
