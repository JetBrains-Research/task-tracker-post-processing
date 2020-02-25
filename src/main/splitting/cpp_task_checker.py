import os
import logging


from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.util.language_util import get_extension_by_language
from src.main.util.file_util import create_file, change_extension_to
from src.main.splitting.task_checker import ITaskChecker, check_call_safely, check_output_safely, TASKS_TESTS_PATH, \
    SOURCE_OBJECT_NAME

log = logging.getLogger(consts.LOGGER_NAME)


class CppTaskChecker(ITaskChecker):

    @property
    def language(self):
        return LANGUAGE.CPP.value

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
        source_code_file = os.path.join(TASKS_TESTS_PATH, SOURCE_OBJECT_NAME,
                                        SOURCE_OBJECT_NAME + get_extension_by_language(self.language))
        create_file(source_code, source_code_file)
        return source_code_file

    def is_source_file_correct(self, source_file: str):
        args = ['g++', '-o', change_extension_to(source_file, '.out'), source_file]
        is_correct = check_call_safely(args, None)
        log.info(f'Source code is correct: {is_correct}')
        return is_correct

    def run_test(self, input: str, expected_output: str, source_file: str):
        args = [change_extension_to(source_file, '.out')]
        return check_output_safely(input, expected_output, args)
