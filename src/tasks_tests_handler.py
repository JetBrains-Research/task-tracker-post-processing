from src import string_helper as sh
from subprocess import Popen, PIPE, call
from src import consts
import os

TASKS_TESTS_PATH = consts.TASKS_TESTS.TASKS_TESTS_PATH.value
SOURCE_FILE_NAME = consts.TASKS_TESTS.SOURCE_FILE_NAME.value
TASKS = consts.TASKS_TESTS.TASKS.value
INPUT_FILE_NAME = consts.TASKS_TESTS.INPUT_FILE_NAME.value


def __create_file(content: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    with open(TASKS_TESTS_PATH + task + '/' + source_file_name + '.' + extension, 'w') as f:
        f.write(content)


def __drop_file(file: str, task: str):
    if os.path.isfile(TASKS_TESTS_PATH + task + '/' + file):
        os.remove(TASKS_TESTS_PATH + task + '/' + file)


def __get_rows_from_file(file: str, task: str):
    with open(TASKS_TESTS_PATH + task + '/' + file, 'r') as f:
        return f.readlines()


# Get input for sending to other process: union list of rows as string
def __get_input(in_file: str, task: str):
    content = __get_rows_from_file(in_file, task)
    return ''.join(content)


def __get_index_out_file_for_in_file(in_file: str, out_files: list):
    # In and out files have similar numbers, for example the in_1 file match to the out_1 file
    return sh.index_containing_substring(out_files, in_file.split('.')[0].split('_')[-1])


def __get_in_and_out_files(list_of_files: list):
    in_files_list = list(filter(lambda file_name: 'in' in file_name and '.txt' in file_name, list_of_files))
    out_files_list = list(filter(lambda file_name: 'out' in file_name and '.txt' in file_name, list_of_files))
    if len(out_files_list) != len(in_files_list):
        raise ValueError('Length of out files list does not equal in files list')

    return in_files_list, out_files_list


def __get_java_class(source_code: str):
    class_key_word = 'class'
    rows = source_code.split('\n')
    for row in rows:
        if class_key_word in row:
            class_index = row.index(class_key_word)
            return row[class_index + len(class_key_word) + 1:].replace(' ', '').replace('{', '')
    raise ValueError('Source code does not contain class name!')


# Wrap all values from input in the print command
def __create_py_input_file(txt_in_file: str, task: str, extension='py', file_name=INPUT_FILE_NAME):
    code = ''
    with open(TASKS_TESTS_PATH + task + '/' + txt_in_file, 'r') as f:
        for line in f:
            code += 'print(' + line.strip('\n') + ')' + '\n'
    __create_file(code, task, extension, file_name)


# For python scripts it is an in file with extension py and for other cases, it is an in file with extension txt
def __get_in_file_for_current_test(cur_in_file: str, task: str, extension='py'):
    if extension == 'py':
        __create_py_input_file(cur_in_file, task)
        return INPUT_FILE_NAME + '.' + extension
    return cur_in_file


# Clear not in\out files for correct program execution
def __clear_old_files(task: str):
    files = next(os.walk(TASKS_TESTS_PATH + task))[2]
    old_files = list(filter(lambda file_name: '.txt' not in file_name, files))
    for file in old_files:
        __drop_file(file, task)


def __run_python_test(in_file: str, out: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    p1 = Popen(['python', TASKS_TESTS_PATH + task + '/' + in_file], stdout=PIPE)
    p2 = Popen(['python', TASKS_TESTS_PATH + task + '/' + source_file_name + '.' + extension], stdin=p1.stdout,
               stdout=PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    if output.decode("utf-8") == out:
        return True
    return False


# Run test for compiled languages
def __run_test(in_file: str, out: str, task: str, popen_args: list):
    p = Popen(popen_args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    cur_out, err = p.communicate(input=__get_input(in_file, task))
    if p.returncode == 0:
        if cur_out == out:
            return True
    return False


def __compile_program(call_args: list):
    if call(call_args) != 0:
        # Error
        return False
    return True


def __get_args_for_running_program(extension: str, task: str, source_file_name: str):
    base_path = TASKS_TESTS_PATH + task + '/'
    call_args = []
    popen_args = []

    if extension == 'java':
        call_args = ['javac', base_path + source_file_name + '.' + extension]
        popen_args = ['java', '-cp', TASKS_TESTS_PATH + task, source_file_name]
    elif extension == 'cpp':
        call_args = ['gcc', '-lstdc++', '-o', base_path + source_file_name + '.out',
                     base_path + source_file_name + '.' + extension]
        popen_args = [base_path + source_file_name + '.out']
    elif extension == 'kt':
        call_args = ['kotlinc', base_path + source_file_name + '.' + extension, '-include-runtime', '-d',
                     base_path + source_file_name + '.jar']
        popen_args = ['java', '-jar', base_path + source_file_name + '.jar']
    return call_args, popen_args


def __create_source_code_file(source_code: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    if extension == 'java':
        source_file_name = __get_java_class(source_code)
    __create_file(source_code, task, extension, source_file_name)
    return source_file_name


# The function returns code run result, was the compilation successful and does the compiled file exist
def __check_test_for_task(source_code: str, in_file: str, out_file: str, task: str, has_compiled_file: bool,
                          is_compiled_successful: bool, extension='py', source_file_name=SOURCE_FILE_NAME):
    is_passed = False
    source_file_name = __create_source_code_file(source_code, task, extension, source_file_name)

    if extension == 'py':
        is_passed = __run_python_test(in_file, __get_rows_from_file(out_file, task)[0], task)
    else:
        if not is_compiled_successful:
            return is_passed, has_compiled_file, is_compiled_successful

        call_args, popen_args = __get_args_for_running_program(extension, task, source_file_name)
        if not has_compiled_file:
            has_compiled_file = True
            is_compiled_successful = __compile_program(call_args)

            if not is_compiled_successful:
                return is_passed, has_compiled_file, is_compiled_successful

        is_passed = __run_test(in_file, __get_rows_from_file(out_file, task)[0], task, popen_args)
    return is_passed, has_compiled_file, is_compiled_successful


def __is_valid_index(index: int):
    return index != -1


def __get_default_compiled_program_info():
    has_compiled_file = False
    is_compiled_successful = True
    return has_compiled_file, is_compiled_successful


def check_task(task: str, source_code: str, extension='py', is_clear=True):
    if is_clear:
        __clear_old_files(task)

    files = next(os.walk(TASKS_TESTS_PATH + task))[2]
    in_files, out_files = __get_in_and_out_files(files)

    count_tests, passed_tests = 0, 0
    has_compiled_file, is_compiled_successful = __get_default_compiled_program_info()

    for cur_in in in_files:
        out_index = __get_index_out_file_for_in_file(cur_in, out_files)
        if not __is_valid_index(out_index):
            continue

        in_file = __get_in_file_for_current_test(cur_in, task, extension)
        out_file = out_files[out_index]
        count_tests += 1

        is_passed, has_compiled_file, is_compiled_successful = __check_test_for_task(source_code, in_file, out_file,
                                                                                     task, has_compiled_file,
                                                                                     is_compiled_successful, extension)
        if is_passed:
            passed_tests += 1

    return count_tests, passed_tests
