# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.util.file_util import change_extension_to
from src.main.splitting.task_checker import ITaskChecker, check_call_safely, check_output_safely, SOURCE_OBJECT_NAME

log = logging.getLogger(consts.LOGGER_NAME)


class CppTaskChecker(ITaskChecker):

    @property
    def language(self):
        return LANGUAGE.CPP

    # #include <iostream>
    # int main(){
    # int a;
    # cin>>a;
    # cout<<a;}
    @property
    def min_symbols_number(self):
        return 60

    @property
    def output_strings(self):
        return ['cout', 'printf']

    def create_source_file(self, source_code: str):
        return self.create_source_file_with_name(source_code, SOURCE_OBJECT_NAME)

    def is_source_file_correct(self, source_file: str):
        args = ['g++', '-o', change_extension_to(source_file, '.out'), source_file]
        is_correct = check_call_safely(args, None)
        log.info(f'Source code is correct: {is_correct}')
        return is_correct

    def run_test(self, input: str, expected_output: str, source_file: str):
        args = [change_extension_to(source_file, '.out')]
        return check_output_safely(input, expected_output, args)
