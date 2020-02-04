import logging
from subprocess import Popen, PIPE, call
from src.main import consts, string_helper as sh
import os

from src.main.activity_tracker_handler import get_extension_by_language
from src.main.consts import TASKS_TESTS, LANGUAGE

TASKS_TESTS_PATH = consts.TASKS_TESTS.TASKS_TESTS_PATH.value
SOURCE_FILE_NAME = consts.TASKS_TESTS.SOURCE_FILE_NAME.value
TASKS = consts.TASKS_TESTS.TASKS.value
INPUT_FILE_NAME = consts.TASKS_TESTS.INPUT_FILE_NAME.value

log = logging.getLogger(consts.LOGGER_NAME)


def __create_file(content: str, task: str, language=LANGUAGE.PYTHON.value, source_file_name=SOURCE_FILE_NAME):
    log.info("Creating file for task " + task + ", language: " + language)
    with open(TASKS_TESTS_PATH + task + '/' + source_file_name + '.' + get_extension_by_language(language), 'w') as f:
        f.write(content)


def __is_file(file: str, task: str):
    return os.path.isfile(TASKS_TESTS_PATH + task + '/' + file)


def __remove_file(file: str, task: str):
    if __is_file(file, task):
        os.remove(TASKS_TESTS_PATH + task + '/' + file)


def __get_content_from_file(file: str, task: str):
    with open(TASKS_TESTS_PATH + task + '/' + file, 'r') as f:
        return f.read().rstrip("\n")


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
    raise ValueError('Source code does not contain class name!')


# Wrap all values from input in the print command
def __create_py_input_file(txt_in_file: str, task: str, file_name=INPUT_FILE_NAME):
    code = ''
    with open(TASKS_TESTS_PATH + task + '/' + txt_in_file, 'r') as f:
        for line in f:
            code += 'print("' + line.strip('\n') + '")' + '\n'
    __create_file(code, task, LANGUAGE.PYTHON.value, file_name)


# For python scripts it is an in file with extension py and for other cases, it is an in file with extension txt
def __get_in_file_for_current_test(cur_in_file: str, task: str, language=LANGUAGE.PYTHON.value):
    if language == LANGUAGE.PYTHON.value:
        __create_py_input_file(cur_in_file, task)
        return INPUT_FILE_NAME + '.' + get_extension_by_language(language)
    return cur_in_file


# Remove not .txt files: we need to remove the generated files (they don't have .txt extension)
def __clear_old_files(task: str):
    files = next(os.walk(TASKS_TESTS_PATH + task))[2]
    old_files = list(filter(lambda file_name: '.txt' not in file_name, files))
    for file in old_files:
        __remove_file(file, task)


def __run_python_test(in_file: str, expected_out: str, task: str, source_file_name=SOURCE_FILE_NAME):
    p1 = Popen(['python3', TASKS_TESTS_PATH + task + '/' + in_file], stdout=PIPE)
    p2 = Popen(['python3',
               TASKS_TESTS_PATH + task + '/' + source_file_name + '.' + get_extension_by_language(LANGUAGE.PYTHON.value)],
               stdin=p1.stdout,
               stdout=PIPE)
    p1.stdout.close()
    actual_out = p2.communicate()[0].decode("utf-8").rstrip("\n")
    log.info("Expected out: " + expected_out + ", actual out: " + actual_out)
    if actual_out == expected_out:
        return True
    return False


# Run test for compiled languages
def __run_test(in_file: str, out: str, task: str, popen_args: list):
    p = Popen(popen_args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    cur_out, err = p.communicate(input=__get_content_from_file(in_file, task))
    if p.returncode == 0 and cur_out.rstrip("\n") == out:
        return True
    return False


def __compile_program(call_args: list):
    if call(call_args) != 0:
        # Error
        return False
    return True


def __get_args_for_running_program(language: str, task: str, source_file_name: str):
    base_path = TASKS_TESTS_PATH + task + '/'
    running_args = []

    if language == LANGUAGE.JAVA.value:
        running_args = ['java', '-cp', TASKS_TESTS_PATH + task, source_file_name]
    elif language == LANGUAGE.CPP.value:
        running_args = [base_path + source_file_name + '.out']
    elif language == LANGUAGE.KOTLIN.value:
        running_args = ['java', '-jar', base_path + source_file_name + '.jar']
    else:
        raise ValueError('Language is not defined')
    return running_args


def __get_args_for_compiling_program(language: str, task: str, source_file_name: str):
    base_path = TASKS_TESTS_PATH + task + '/'
    extension = get_extension_by_language(language)

    if language == LANGUAGE.JAVA.value:
        compiled_file_path = base_path + source_file_name + '.' + extension
        call_args = ['javac', compiled_file_path]
    elif language == LANGUAGE.CPP.value:
        compiled_file_path = base_path + source_file_name + '.out'
        call_args = ['gcc', '-lstdc++', '-o', compiled_file_path, base_path + source_file_name + '.' + extension]
    elif language == LANGUAGE.KOTLIN.value:
        compiled_file_path = base_path + source_file_name + '.jar'
        call_args = ['kotlinc', base_path + source_file_name + '.' + extension, '-include-runtime', '-d',
                     compiled_file_path]
    else:
        raise ValueError('Language is not defined')

    return call_args


def __create_source_code_file(source_code: str, task: str, language=LANGUAGE.PYTHON.value, source_file_name=SOURCE_FILE_NAME):
    if language == LANGUAGE.JAVA.value:
        source_file_name = __get_java_class(source_code)
    __create_file(source_code, task, language, source_file_name)
    return source_file_name


# The function returns code run result, was the compilation successful and does the compiled file exist
def __check_test_for_task(in_file: str, out_file: str, task: str, language=LANGUAGE.PYTHON.value, source_file_name=SOURCE_FILE_NAME):
    if language == LANGUAGE.PYTHON.value:
        is_passed = __run_python_test(in_file, __get_content_from_file(out_file, task), task)
    else:
        running_args = __get_args_for_running_program(language, task, source_file_name)
        is_passed = __run_test(in_file, __get_content_from_file(out_file, task), task, running_args)
    return is_passed


def __is_valid_index(index: int):
    return index != -1


def __get_default_compiled_program_info(source_file_name: str, task: str):
    has_compiled_file = __is_file(source_file_name, task)
    is_compiled_successful = True
    return has_compiled_file, is_compiled_successful


def check_task(task: str, source_code: str, language=LANGUAGE.PYTHON.value, to_clear=True):
    log.info("Start checking task " + task + " for source code on " + language + ":\n" + source_code)
    if to_clear:
        __clear_old_files(task)

    files = next(os.walk(TASKS_TESTS_PATH + task))[2]
    in_and_out_files = __get_in_and_out_files(files)

    count_tests, passed_tests = len(in_and_out_files), 0
    source_file_name = __create_source_code_file(source_code, task, language)

    if language != LANGUAGE.PYTHON.value:
        has_compiled_file, is_compiled_successful = __get_default_compiled_program_info(source_file_name, task)

        if not has_compiled_file:
            log.info("Source code for task " + task + " doesn't have compiled file")
            compiling_args = __get_args_for_compiling_program(language, task, source_file_name)
            is_compiled_successful = __compile_program(compiling_args)

        if not is_compiled_successful:
            log.info("Source code for task " + task + " wasn't compiled successful")
            log.info("Finish checking task " + task + ", " + str(passed_tests) + "/" + str(count_tests) + " are passed")
            return count_tests, passed_tests

    for cur_in, cur_out in in_and_out_files:
        in_file = __get_in_file_for_current_test(cur_in, task, language)
        is_passed = __check_test_for_task(in_file, cur_out, task, language, source_file_name)
        log.info("Test " + cur_in + " for task " + task + " is passed: " + str(is_passed))
        if is_passed:
            passed_tests += 1

    log.info("Finish checking task " + task + ", " + str(passed_tests) + "/" + str(count_tests) + " are passed")
    return count_tests, passed_tests


def get_most_likely_tasks(source_code: str, language: str):
    most_likely_tasks = []
    max_rate = 0
    for task in TASKS_TESTS.TASKS.value:
        count_tests, passed_tests = check_task(task, source_code, language, to_clear=False)
        passed_rate = passed_tests / count_tests
        if passed_rate > max_rate:
            max_rate = passed_rate
            most_likely_tasks = [task]
        elif passed_rate == max_rate:
            most_likely_tasks.append(task)

    return most_likely_tasks, max_rate

