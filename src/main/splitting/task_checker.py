# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Optional
from subprocess import check_output, CalledProcessError, check_call, TimeoutExpired, STDOUT

from src.main.util.log_util import log_and_raise_error
from src.main.util.language_util import get_extension_by_language
from src.main.util.strings_util import contains_any_of_substrings
from src.main.util.consts import TASK, TIMEOUT, TASKS_TESTS, LOGGER_NAME, LANGUAGE, TEST_RESULT
from src.main.util.file_util import get_content_from_file, remove_directory, create_directory, create_file

# For each TASK we have in_file (str) and out_file(str) for testing
FilesDict = Dict[TASK, List[Tuple[str, str]]]

TASKS_TESTS_PATH = TASKS_TESTS.TASKS_TESTS_PATH.value
SOURCE_OBJECT_NAME = TASKS_TESTS.SOURCE_OBJECT_NAME.value
SOURCE_FOLDER = os.path.join(TASKS_TESTS_PATH, SOURCE_OBJECT_NAME)

log = logging.getLogger(LOGGER_NAME)


# Returns False if time is out, because it means that the output cannot be gotten and thus
# the expected output doesn't match the real one
def check_output_safely(input: str, expected_output: str, popen_args: List[str], timeout_return: bool = False) -> bool:
    try:
        actual_out = check_output(popen_args, input=input, universal_newlines=True, timeout=TIMEOUT)
        actual_out = actual_out.rstrip('\n')
        log.info(f'Expected out: {expected_output}, actual out: {actual_out}')
        return actual_out == expected_output
    except CalledProcessError as e:
        log.exception(e)
        return False
    except TimeoutExpired as e:
        log.exception(e)
        return timeout_return


# Returns True if time is out, because it means that no other errors were raised,
# so in case of code correctness checking it means that code is correct
def check_call_safely(call_args: List[str], timeout: Optional[int] = TIMEOUT, timeout_return: bool = True,
                      shell: Optional[bool] = None) -> bool:
    try:
        if shell is not None:
            check_call(call_args, timeout=timeout, shell=shell)
        else:
            check_call(call_args, timeout=timeout)
        return True
    except CalledProcessError as e:
        log.exception(e)
        return False
    except TimeoutExpired as e:
        log.exception(e)
        return timeout_return


def remove_compiled_files() -> None:
    remove_directory(SOURCE_FOLDER)
    create_directory(SOURCE_FOLDER)


class ITaskChecker(object, metaclass=ABCMeta):
    @property
    @abstractmethod
    def language(self) -> LANGUAGE:
        raise NotImplementedError

    @property
    @abstractmethod
    def min_symbols_number(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def output_strings(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def create_source_file(self, source_code: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def is_source_file_correct(self, source_file: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def run_test(self, input: str, expected_output: str, source_file: str) -> bool:
        raise NotImplementedError

    @staticmethod
    def get_no_need_to_run_tests_values(rate: float, tasks_len: int) -> Tuple[bool, List[float]]:
        need_to_run_tests = False
        test_results = [rate] * tasks_len
        return need_to_run_tests, test_results

    def create_source_file_with_name(self, source_code: str, name: str) -> str:
        source_code_file = os.path.join(TASKS_TESTS_PATH, SOURCE_OBJECT_NAME,
                                        name + get_extension_by_language(self.language).value)
        create_file(source_code, source_code_file)
        return source_code_file

    # We don't want to run tests if source file is incorrect, too small, or doesn't have any output, so here
    # we check if any of these conditions are met
    # Returns do we have to run tests (bool), current tests results (List[float]), and rate (float)
    def check_before_tests(self, source_file: str, source_code: str, tasks: List[TASK]) -> (bool, List[float], float):
        test_results = []
        need_to_run_tests = True
        rate = TEST_RESULT.CORRECT_CODE.value

        # not to check incorrect fragments
        if not self.is_source_file_correct(source_file):
            rate = TEST_RESULT.INCORRECT_CODE.value
            need_to_run_tests, test_results = self.get_no_need_to_run_tests_values(rate, len(tasks))

        # not to check too small fragments because they cannot return true anyway
        elif len(source_code) < self.min_symbols_number:
            log.info('Code fragment is too small')
            need_to_run_tests, test_results = self.get_no_need_to_run_tests_values(rate, len(tasks))

        # not to check fragments without output because they cannot return anything
        elif not contains_any_of_substrings(source_code, self.output_strings):
            log.info('Code fragment does not contain any output strings')
            need_to_run_tests, test_results = self.get_no_need_to_run_tests_values(rate, len(tasks))

        return need_to_run_tests, test_results, rate

    def check_task(self, task: TASK, in_and_out_files_dict:  FilesDict, source_file: str,
                   stop_after_first_false = True) -> float:
        log.info(f'Start checking task {task.value}')
        in_and_out_files = in_and_out_files_dict.get(task)
        if not in_and_out_files:
            log_and_raise_error(f'Task data for the {task.value} does not exist', log)

        counted_tests, passed_tests = len(in_and_out_files), 0
        for in_file, out_file in in_and_out_files:
            is_passed = self.run_test(get_content_from_file(in_file), get_content_from_file(out_file), source_file)
            log.info(f'Test {in_file} for task {task.value} is passed: {str(is_passed)}')
            if is_passed:
                passed_tests += 1
            elif stop_after_first_false:
                # keep existing rate, even if it's not 0, to save the information about partly passed tests
                log.info('Stop after first false')
                break

        rate = passed_tests / counted_tests
        log.info(f'Finish checking task {task.value}, rate: {str(rate)}')
        return rate

    def check_tasks(self, tasks: List[TASK], source_code: str, in_and_out_files_dict: FilesDict,
                    stop_after_first_false: bool = True) -> List[float]:
        remove_compiled_files()
        log.info(f'Starting checking tasks {[t.value for t in tasks]}'
                 f' for source code on {self.language.value}:\n{source_code}')
        source_file = self.create_source_file(source_code)
        need_to_run_tests, test_results, rate = self.check_before_tests(source_file, source_code, tasks)

        if not need_to_run_tests:
            log.info(f'Finish checking tasks, test results: {str(test_results)}')
            return test_results

        for task in tasks:
            test_results.append(self.check_task(task, in_and_out_files_dict, source_file, stop_after_first_false))

        log.info(f'Finish checking tasks, test results: {str(test_results)}')
        return test_results
