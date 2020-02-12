import os
import ast
import signal
import logging
from subprocess import Popen, PIPE, call

from src.main.util import consts
from src.main.util.consts import LANGUAGE, TASK
from src.main.preprocessing.activity_tracker_handler import get_extension_by_language
from src.main.util.file_util import remove_file, get_content_from_file, create_file, create_directory, remove_directory

INPUT_FILE_NAME = consts.TASKS_TESTS.INPUT_FILE_NAME.value
TASKS_TESTS_PATH = consts.TASKS_TESTS.TASKS_TESTS_PATH.value
SOURCE_OBJECT_NAME = consts.TASKS_TESTS.SOURCE_OBJECT_NAME.value

log = logging.getLogger(consts.LOGGER_NAME)


class TimeoutException(Exception):   # Custom exception class
    pass


def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException


# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)


def __get_task_file(file: str, task: str):
    return TASKS_TESTS_PATH + task + '/' + file


def __get_compiled_file(file: str):
    return __get_source_folder() + '/' + file


def __get_source_folder():
    return TASKS_TESTS_PATH + SOURCE_OBJECT_NAME


def __get_in_and_out_files(list_of_files: list):
    in_files_list = list(filter(lambda file_name: 'in' in file_name and '.txt' in file_name, list_of_files))
    out_files_list = list(filter(lambda file_name: 'out' in file_name and '.txt' in file_name, list_of_files))
    if len(out_files_list) != len(in_files_list):
        raise ValueError('Length of out files list does not equal in files list')
    in_and_out_pairs = __separate_in_and_out_files_on_pairs(in_files_list, out_files_list)
    return in_and_out_pairs


def __get_out_file_by_in_file(in_file: str):
    return 'out_' + str(in_file.split('.')[0].split('_')[-1]) + '.txt'


def __separate_in_and_out_files_on_pairs(in_files: list, out_files: list):
    pairs = []
    for in_file in in_files:
        out_file = __get_out_file_by_in_file(in_file)
        if out_file not in out_files:
            raise ValueError('List of out files does not contain a file for ' + in_file)
        pairs.append((in_file, out_file))
    return pairs


def __get_java_class(source_code: str):
    class_key_word = 'class'
    rows = source_code.split('\n')
    for row in rows:
        if class_key_word in row:
            class_index = row.index(class_key_word)
            return row[class_index + len(class_key_word) + 1:].replace(' ', '').replace('{', '')
    return SOURCE_OBJECT_NAME


# Wrap all values from input in the print command
def __create_py_input_file(txt_in_file: str, task: str, file_name=INPUT_FILE_NAME):
    code = ''
    with open(__get_task_file(txt_in_file, task), 'r') as f:
        for line in f:
            code += 'print("' + line.strip('\n') + '")' + '\n'
    create_file(code, get_extension_by_language(LANGUAGE.PYTHON.value), __get_task_file(file_name, task))


# For python scripts it is an in file with extension py and for other cases, it is an in file with extension txt
def __get_in_file_for_current_test(cur_in_file: str, task: str, language=LANGUAGE.PYTHON.value):
    if language == LANGUAGE.PYTHON.value:
        __create_py_input_file(cur_in_file, task)
        return INPUT_FILE_NAME + '.' + get_extension_by_language(language)
    return cur_in_file


def __remove_compiled_files():
    remove_directory(__get_source_folder())
    create_directory(__get_source_folder())


def __run_python_test(in_file: str, expected_out: str, task: str, source_file_name=SOURCE_OBJECT_NAME):
    p1 = Popen(['python3', __get_task_file(in_file, task)], stdout=PIPE)
    p2 = Popen(['python3', __get_compiled_file(source_file_name) + '.'
                + get_extension_by_language(LANGUAGE.PYTHON.value)],
               stdin=p1.stdout,
               stdout=PIPE)
    p1.stdout.close()
    try:
        out, err = p2.communicate()
        actual_out = out.decode("utf-8").rstrip("\n")
        log.info("In-file: " + in_file + ", task: " + task + ", expected out: " + expected_out + ", actual out: " + actual_out)
        return p2.returncode != 0, actual_out == expected_out
    except:
        log.info("In-file: " + in_file + ", task: " + task + ", error!")


# Run test for compiled languages
def __run_test(in_file: str, expected_out: str, task: str, popen_args: list):
    p = Popen(popen_args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    out, err = p.communicate(input=get_content_from_file(__get_task_file(in_file, task)))
    actual_out = out.rstrip("\n")
    log.info("In-file: " + in_file + ", task: " + task + ", expected out: " + expected_out + ", actual out: " + actual_out)
    return p.returncode != 0, actual_out == expected_out


def __compile_program(call_args: list):
    return call(call_args) == 0


def __get_args_for_running_program(language: str, source_file_name: str):
    if language == LANGUAGE.JAVA.value:
        running_args = ['java', '-cp', __get_source_folder(), source_file_name]

    elif language == LANGUAGE.CPP.value:
        running_args = [__get_compiled_file(source_file_name) + '.out']
    elif language == LANGUAGE.KOTLIN.value:
        running_args = ['java', '-jar', __get_compiled_file(source_file_name) + '.jar']
    else:
        raise ValueError('Language is not defined')
    return running_args


def __get_args_for_compiling_program(language: LANGUAGE, source_file_name: str):
    compiled_file = __get_compiled_file(source_file_name)
    extension = get_extension_by_language(language)

    if language == LANGUAGE.JAVA.value:
        compiled_file_path = compiled_file + '.' + extension
        call_args = ['javac', compiled_file_path]
    elif language == LANGUAGE.CPP.value:
        compiled_file_path = compiled_file + '.out'
        call_args = ['g++', '-o', compiled_file_path, compiled_file + '.' + extension]
    elif language == LANGUAGE.KOTLIN.value:
        compiled_file_path = compiled_file + '.jar'
        call_args = ['kotlinc', compiled_file + '.' + extension, '-include-runtime', '-d',
                     compiled_file_path]
    else:
        raise ValueError('Language is not defined')

    return call_args


def __create_source_code_file(source_code: str, language=LANGUAGE.PYTHON.value,
                              source_file_name=SOURCE_OBJECT_NAME):
    if language == LANGUAGE.JAVA.value:
        source_file_name = __get_java_class(source_code)
    create_file(source_code, get_extension_by_language(language), __get_compiled_file(source_file_name))
    return source_file_name


def create_in_and_out_dict(tasks: list):
    in_and_out_files_dict = {}
    for task in tasks:
        files = next(os.walk(TASKS_TESTS_PATH + task))[2]
        in_and_out_files_dict[task] = __get_in_and_out_files(files)

    return in_and_out_files_dict


def is_python_file_correct(filename: str):
    source = open(filename, 'r').read() + '\n'
    try:
        code = compile(source, filename, 'exec')
        # todo: remove consts
        signal.alarm(5)
        eval(code, {})
        return True
    except TimeoutException:
        log.info("Time is out")
        return is_valid_python_file(filename)
    except:
        return False


def is_valid_python_file(file_name):
    call_args = ['mypy', file_name]
    is_valid = __compile_program(call_args)
    return is_valid


def is_source_file_correct(source_file, language=LANGUAGE.PYTHON.value):
    if language == LANGUAGE.PYTHON.value:
        is_correct = is_python_file_correct(__get_compiled_file(source_file) + "." + get_extension_by_language(language))
    else:
        compiling_args = __get_args_for_compiling_program(language, source_file)
        is_correct = __compile_program(compiling_args)
    log.info("Source code is correct: " + str(is_correct))
    return is_correct


def check_tasks(tasks: list, source_code: str, in_and_out_files_dict: dict, language=LANGUAGE.PYTHON.value):
    test_results = []
    __remove_compiled_files()
    source_file = __create_source_code_file(source_code, language)
    log.info("Starting checking tasks " + str(tasks) + "for source code on " + language + ":\n" + source_code)

    rate = -1
    if not is_source_file_correct(source_file, language):
        test_results = [rate] * len(tasks)
        log.info("Finish checking tasks, test results: " + str(test_results))
        return test_results

    rate = 0
    # not to check too small fragments, because they cannot return true anyway
    # todo: remove const
    if len(source_code) < 10:
        test_results = [rate] * len(tasks)
        log.info("Code fragment is too small")
        log.info("Finish checking tasks, test results: " + str(test_results))
        return test_results

    for task in tasks:
        log.info("Start checking task " + task)
        in_and_out_files = in_and_out_files_dict.get(task)
        if in_and_out_files is None:
            raise ValueError('Task data for the ' + task + ' is not exist')

        counted_tests, passed_tests = len(in_and_out_files), 0
        for cur_in, cur_out in in_and_out_files:
            in_file = __get_in_file_for_current_test(cur_in, task, language)
            task_file = __get_task_file(cur_out, task)
            if language == LANGUAGE.PYTHON.value:
                has_error, is_passed = __run_python_test(in_file, get_content_from_file(task_file), task)
            else:
                running_args = __get_args_for_running_program(language, source_file)
                has_error, is_passed = __run_test(in_file, get_content_from_file(task_file), task, running_args)

            log.info("Test " + cur_in + " for task " + task + " is passed: " + str(is_passed))
            if is_passed:
                passed_tests += 1

        rate = passed_tests / counted_tests
        log.info("Finish checking task " + task + ", rate: " + str(rate))
        test_results.append(rate)

    log.info("Finish checking tasks, test results: " + str(test_results))
    return test_results
