# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.util.file_util import change_extension_to
from src.main.splitting.task_checker import ITaskChecker, check_call_safely, check_output_safely, SOURCE_OBJECT_NAME

log = logging.getLogger(consts.LOGGER_NAME)


class KotlinTaskChecker(ITaskChecker):

    @property
    def language(self):
        return LANGUAGE.KOTLIN

    # fun main(args: Array<String>){
    # val a:Int=readLine()!!.toInt()
    # print(a)}
    @property
    def min_symbols_number(self):
        return 80

    @property
    def output_strings(self):
        return ['print']

    def create_source_file(self, source_code: str):
        return self.create_source_file_with_name(source_code, SOURCE_OBJECT_NAME)

    def is_source_file_correct(self, source_file: str):
        args = ['kotlinc', source_file, '-include-runtime', '-d', change_extension_to(source_file, '.jar')]
        # to be sure there is enough time to create a jar, call is checked with timeout=None;
        # there was 'Error: Invalid or corrupt jarfile' even with 5 sec timeout
        is_correct = check_call_safely(args, None)
        log.info(f'Source code is correct: {is_correct}')
        return is_correct

    def run_test(self, input: str, expected_output: str, source_file: str):
        args = ['java', '-jar', change_extension_to(source_file, '.jar')]
        return check_output_safely(input, expected_output, args)
