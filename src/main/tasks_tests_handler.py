from subprocess import Popen, PIPE, call
from src.main import consts, string_helper as sh
import os

TASKS_TESTS_PATH = consts.TASKS_TESTS.TASKS_TESTS_PATH.value
SOURCE_FILE_NAME = consts.TASKS_TESTS.SOURCE_FILE_NAME.value
TASKS = consts.TASKS_TESTS.TASKS.value
INPUT_FILE_NAME = consts.TASKS_TESTS.INPUT_FILE_NAME.value


def __create_file(content: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    with open(TASKS_TESTS_PATH + task + '/' + source_file_name + '.' + extension, 'w') as f:
        f.write(content)


def __is_file(file: str, task: str):
    return os.path.isfile(TASKS_TESTS_PATH + task + '/' + file)


def __remove_file(file: str, task: str):
    if __is_file(file, task):
        os.remove(TASKS_TESTS_PATH + task + '/' + file)


def __get_content_from_file(file: str, task: str):
    with open(TASKS_TESTS_PATH + task + '/' + file, 'r') as f:
        return f.read().rstrip("\n")


def __get_out_file_index_for_in_file(in_file: str, out_files: list):
    # In and out files have the same indices, for example the in_1 file matches with the out_1 file
    return sh.index_containing_substring(out_files, in_file.split('.')[0].split('_')[-1])


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


def __is_python(extension: str):
    return extension == 'py'


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
    if __is_python(extension):
        __create_py_input_file(cur_in_file, task)
        return INPUT_FILE_NAME + '.' + extension
    return cur_in_file


# Clear not .txt files: we need to clear the generated files (it has not .txt extension)
def __clear_old_files(task: str):
    files = next(os.walk(TASKS_TESTS_PATH + task))[2]
    old_files = list(filter(lambda file_name: '.txt' not in file_name, files))
    for file in old_files:
        __remove_file(file, task)


def __run_python_test(in_file: str, out: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    p1 = Popen(['python', TASKS_TESTS_PATH + task + '/' + in_file], stdout=PIPE)
    p2 = Popen(['python', TASKS_TESTS_PATH + task + '/' + source_file_name + '.' + extension], stdin=p1.stdout,
               stdout=PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    if output.decode("utf-8").rstrip("\n") == out:
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


def __get_compiled_file_path(extension: str, task: str, source_file_name: str):
    base_path = TASKS_TESTS_PATH + task + '/'
    compiled_file_path = None
    if extension == 'java':
        compiled_file_path = base_path + source_file_name + '.' + extension
    elif extension == 'cpp':
        compiled_file_path = base_path + source_file_name + '.out'
    elif extension == 'kt':
        compiled_file_path = base_path + source_file_name + '.jar'
    return compiled_file_path


def __get_args_for_running_program(extension: str, task: str, source_file_name: str):
    base_path = TASKS_TESTS_PATH + task + '/'
    running_args = []

    if extension == 'java':
        running_args = ['java', '-cp', TASKS_TESTS_PATH + task, source_file_name]
    elif extension == 'cpp':
        running_args = [base_path + source_file_name + '.out']
    elif extension == 'kt':
        running_args = ['java', '-jar', base_path + source_file_name + '.jar']
    return running_args


def __get_args_for_compiling_program(extension: str, task: str, source_file_name: str):
    compiled_file_path = __get_compiled_file_path(extension, task, source_file_name)
    base_path = TASKS_TESTS_PATH + task + '/'
    call_args = []

    if extension == 'java':
        call_args = ['javac', compiled_file_path]
    elif extension == 'cpp':
        call_args = ['gcc', '-lstdc++', '-o', compiled_file_path, base_path + source_file_name + '.' + extension]
    elif extension == 'kt':
        call_args = ['kotlinc', base_path + source_file_name + '.' + extension, '-include-runtime', '-d',
                     compiled_file_path]
    return call_args


def __create_source_code_file(source_code: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    if extension == 'java':
        source_file_name = __get_java_class(source_code)
    __create_file(source_code, task, extension, source_file_name)
    return source_file_name


# The function returns code run result, was the compilation successful and does the compiled file exist
def __check_test_for_task(in_file: str, out_file: str, task: str, extension='py', source_file_name=SOURCE_FILE_NAME):
    if __is_python(extension):
        is_passed = __run_python_test(in_file, __get_content_from_file(out_file, task), task)
    else:
        running_args = __get_args_for_running_program(extension, task, source_file_name)
        is_passed = __run_test(in_file, __get_content_from_file(out_file, task), task, running_args)
    return is_passed


def __is_valid_index(index: int):
    return index != -1


def __get_default_compiled_program_info(source_file_name: str, task: str):
    has_compiled_file = __is_file(source_file_name, task)
    is_compiled_successful = True
    return has_compiled_file, is_compiled_successful


def check_task(task: str, source_code: str, extension='py', to_clear=True):
    if to_clear:
        __clear_old_files(task)

    files = next(os.walk(TASKS_TESTS_PATH + task))[2]
    in_and_out_files = __get_in_and_out_files(files)

    count_tests, passed_tests = len(in_and_out_files), 0
    source_file_name = __create_source_code_file(source_code, task, extension)

    if not __is_python(extension):
        has_compiled_file, is_compiled_successful = __get_default_compiled_program_info(source_file_name, task)

        compiling_args = __get_args_for_compiling_program(extension, task, source_file_name)
        if not has_compiled_file:
            is_compiled_successful = __compile_program(compiling_args)

        if not is_compiled_successful:
            return count_tests, passed_tests

    for cur_in, cur_out in in_and_out_files:
        in_file = __get_in_file_for_current_test(cur_in, task, extension)
        is_passed = __check_test_for_task(in_file, cur_out, task, extension, source_file_name)
        if is_passed:
            passed_tests += 1

    return count_tests, passed_tests
