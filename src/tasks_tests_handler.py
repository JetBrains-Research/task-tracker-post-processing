from src import string_helper as sh
from subprocess import Popen, PIPE, call
from src import consts
import os

TASKS_TESTS_PATH = './resources/tasks_tests/'
SOURCE_FILE_NAME = 'source'
TASKS = ['pies', 'max_3', 'zero', 'election', 'brackets', 'max_digit']
INPUT_FILE_NAME = 'in'


def __get_extension_by_language(items_dict: dict, language: str):
    extensions = [k for k, v in items_dict.items() if v == language]
    print(extensions)
    pass


def __create_source_code_file(source_code: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    with open(TASKS_TESTS_PATH + task + '/' + source_file_name + '.' + extension, 'w') as f:
        f.write(source_code)


def __drop_file(file: str, task: str):
    os.remove(TASKS_TESTS_PATH + task + '/' + file)


# Get the rows from file for comparing it with a program result
def __get_rows_from_file(out_file: str, task: str):
    with open(TASKS_TESTS_PATH + task + '/' + out_file, 'r') as f:
        return f.readlines()


def __get_input(in_file: str, task: str):
    content = __get_rows_from_file(in_file, task)
    return ''.join(content)


def __get_index_out_file_for_in_file(in_file: str, out_files: list):
    # In and out files have similar numbers, for example the in_1 file match to the out_1 file
    return sh.index_containing_substring(out_files, in_file.split('.')[0].split('_')[-1])


def __separate_in_and_out_files(list_of_files: list):
    in_files_list = list(filter(lambda file_name: 'in' in file_name, list_of_files))
    out_files_list = list(filter(lambda file_name: 'out' in file_name, list_of_files))
    if len(out_files_list) != len(in_files_list):
        raise ValueError('Length of out files list does not equal in files list')

    return in_files_list, out_files_list


def __run_python_test(in_file: str, out: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    p1 = Popen(['python', TASKS_TESTS_PATH + task + '/' + in_file], stdout=PIPE)
    p2 = Popen(['python', TASKS_TESTS_PATH + task + '/' + source_file_name + '.' + extension], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    if output.decode("utf-8") == out:
        return True
    return False


def __get_java_class(source_code: str):
    class_key_word = 'class'
    rows = source_code.split('\n')
    for row in rows:
        if class_key_word in row:
            class_index = row.index(class_key_word)
            return row[class_index + len(class_key_word) + 1:].replace(' ', '').replace('{', '')
    raise ValueError('Source code does not contain class name!')


def __run_java_test(in_file: str, out: str, task: str, source_file_name=SOURCE_FILE_NAME, extension='java'):
    source_path = TASKS_TESTS_PATH + task + '/' + source_file_name + '.' + extension
    if call(['javac', source_path]) != 0:
        # Error
        return False

    p = Popen(['java', '-cp', TASKS_TESTS_PATH + task, source_file_name],
              stdin=PIPE, stdout=PIPE, stderr=PIPE,
              universal_newlines=True)
    cur_out, err = p.communicate(input=__get_input(in_file, task))
    if p.returncode == 0:
        if cur_out == out:
            return True
    return False


def __check_test_for_task(source_code: str, in_file: str, out_file: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    if extension == 'java':
        source_file_name = __get_java_class(source_code)
    __create_source_code_file(source_code, task, extension, source_file_name)
    res = False
    # Todo: add other languages
    if extension == 'py':
        res = __run_python_test(in_file, __get_rows_from_file(out_file, task)[0], task)
    elif extension == 'java':
        res = __run_java_test(in_file, __get_rows_from_file(out_file, task)[0], task, source_file_name)
    __drop_file(source_file_name + '.' + extension, task)
    if extension == 'java':
        __drop_file(source_file_name + '.' + 'class', task)
    return res


# Wrap all values from input in the print command
def __create_py_input_file(txt_in_file: str, task: str, extension='py', file_name=INPUT_FILE_NAME):
    code = ''
    with open(TASKS_TESTS_PATH + task + '/' + txt_in_file, 'r') as f:
        for line in f:
            code += 'print(' + line.strip('\n') + ')' + '\n'
    __create_source_code_file(code, task, extension, file_name)


# For python scripts it is an in file with extension py and for other cases, it is an in file with extension txt
def __get_test_in_file(out_index: int, cur_in_file: str, extension='py'):
    if extension == 'py':
        return INPUT_FILE_NAME + '.' + extension
    return cur_in_file


# Clear not in\out files for correct program execution
def __clear_old_files(task: str):
    files = next(os.walk(TASKS_TESTS_PATH + task))[2]
    old_files = list(filter(lambda file_name: '.txt' not in file_name, files))
    for file in old_files:
        __drop_file(file, task)


def check_task(task: str, source_code: str, extension='py'):
    __clear_old_files(task)
    files = next(os.walk(TASKS_TESTS_PATH + task))[2]
    in_files, out_files = __separate_in_and_out_files(files)
    count_tests = 0
    passed_tests = 0

    for cur_in in in_files:
        if extension == 'py':
            __create_py_input_file(cur_in, task)
        out_index = __get_index_out_file_for_in_file(cur_in, out_files)
        if out_index == -1:
            continue
        test_in = __get_test_in_file(out_index, cur_in, extension)
        count_tests += 1
        res = __check_test_for_task(source_code, test_in,
                                    out_files[__get_index_out_file_for_in_file(cur_in, out_files)], task, extension)
        if res:
            passed_tests += 1
    if extension == 'py':
        __drop_file(INPUT_FILE_NAME + '.' + extension, task)
    return count_tests, passed_tests


code_1 = 'a = int(input())\nb = int(input())\nn = int(input())\nprint(str(a * n) + " " + str((b * n)))'
code_2 = 'a = int(input())\nb = int(input())\nn = int(input())\nprint(str(a * n) + " " + str((b * n)))'
code_3 = 'a = int(input())\nb = int(input())\nn = int(input())\nprint(str(a * n) + " " + str((b * n)))'
java_code_1 = 'import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader(System.in);\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n        System.out.println(a * n + " " + b * n);\n    }\n}'
print(check_task('pies', java_code_1, extension='java'))


