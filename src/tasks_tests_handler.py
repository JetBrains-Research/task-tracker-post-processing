from src import string_helper as sh
from subprocess import Popen, PIPE
import os

TASKS_TESTS_PATH = './resources/tasks_tests/'
SOURCE_FILE_NAME = 'source.py'
TASKS = ['pies', 'max_3', 'zero', 'election', 'brackets', 'max_digit']
PYTHON_INPUT_FILE_NAME = 'in.py'


def __create_source_code_file(source_code: str, task: str, source_file_name=SOURCE_FILE_NAME):
    with open(TASKS_TESTS_PATH + task + '/' + source_file_name, 'w') as f:
        f.write(source_code)


def __drop_source_code_file(source_code_file: str, task: str):
    os.remove(TASKS_TESTS_PATH + task + '/' + source_code_file)


def __get_out_from_out_file(out_file: str):
    with open(TASKS_TESTS_PATH + 'pies' + '/' + out_file, 'r') as f:
        return f.readline()


def __get_index_out_file_for_in_file(in_file: str, out_files: list):
    return sh.index_containing_substring(out_files, in_file.split('.')[0].split('_')[-1])


def __separate_in_and_out_files(list_of_files: list):
    in_files_list = list(filter(lambda file_name: 'in' in file_name, list_of_files))
    out_files_list = list(filter(lambda file_name: 'out' in file_name, list_of_files))
    if len(out_files_list) != len(in_files_list):
        raise ValueError('Length of out files list does not equal in files list')

    return in_files_list, out_files_list


def __run_test(in_file: str, out: str, task: str):
    p1 = Popen(['python', TASKS_TESTS_PATH + task + '/' + in_file], stdout=PIPE)
    p2 = Popen(['python', TASKS_TESTS_PATH + task + '/' + SOURCE_FILE_NAME], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    if output.decode("utf-8") == out:
        return True
    return False


def __check_test_for_task(source_code: str, in_file: str, out_file: str, task: str):
    __create_source_code_file(source_code, task)
    res = __run_test(in_file, __get_out_from_out_file(out_file), task)
    __drop_source_code_file(SOURCE_FILE_NAME, task)
    return res


def __create_py_input_file(txt_in_file: str, task: str, file_name=PYTHON_INPUT_FILE_NAME):
    code = ''
    with open(TASKS_TESTS_PATH + task + '/' + txt_in_file, 'r') as f:
        for line in f:
            code += 'print(' + line.strip('\n') + ')' + '\n'
    __create_source_code_file(code, task, file_name)


def check_task(task: str, source_code: str):
    files = next(os.walk(TASKS_TESTS_PATH + task))[2]
    in_files, out_files = __separate_in_and_out_files(files)
    count_tests = 0
    passed_tests = 0

    for cur_in in in_files:
        __create_py_input_file(cur_in, task)
        out_index = __get_index_out_file_for_in_file(cur_in, out_files)
        if out_index == -1:
            continue
        count_tests += 1
        res = __check_test_for_task(source_code, PYTHON_INPUT_FILE_NAME,
                                    out_files[__get_index_out_file_for_in_file(cur_in, out_files)],task)
        if res:
            passed_tests += 1
    __drop_source_code_file(PYTHON_INPUT_FILE_NAME, task)
    return count_tests, passed_tests


code_1 = 'a = int(input())\nb = int(input())\nn = int(input())\nprint(str(a * n) + " " + str((b * n)))'
code_2 = 'a = int(input())\nb = int(input())\nc = int(input())\nprint(max(a, b, c))'
print(check_task('pies', code_2))