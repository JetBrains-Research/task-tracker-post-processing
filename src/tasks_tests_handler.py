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
    if os.path.isfile(TASKS_TESTS_PATH + task + '/' + file):
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
    __create_source_code_file(code, task, extension, file_name)


# For python scripts it is an in file with extension py and for other cases, it is an in file with extension txt
def __get_test_in_file(cur_in_file: str, extension='py'):
    if extension == 'py':
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
def __run_test(in_file: str, out: str, task: str, call_args: list, popen_args: list):
    if call(call_args) != 0:
        # Error
        return False

    p = Popen(popen_args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    cur_out, err = p.communicate(input=__get_input(in_file, task))
    if p.returncode == 0:
        if cur_out == out:
            return True
    return False


# Drop files: with source code and compiled files
def __drop_program_files(source_file_name: str, extension: str, task: str, compiled_file_extension=None):
    if compiled_file_extension is not None:
        __drop_file(source_file_name + compiled_file_extension, task)
    __drop_file(source_file_name + '.' + extension, task)


def __get_args_for_run_programs(extension: str, task: str, source_file_name: str):
    base_path = TASKS_TESTS_PATH + task + '/'
    compiled_file_extension = None
    call_args = []
    popen_args = []

    if extension == 'java':
        compiled_file_extension = '.class'
        call_args = ['javac', base_path + source_file_name + '.' + extension]
        popen_args = ['java', '-cp', TASKS_TESTS_PATH + task, source_file_name]
    elif extension == 'cpp':
        compiled_file_extension = '.out'
        call_args = ['gcc', '-lstdc++', '-o', base_path + source_file_name + '.out',
                     base_path + source_file_name + '.' + extension]
        popen_args = [base_path + source_file_name + compiled_file_extension]
    elif extension == 'kt':
        compiled_file_extension = '.jar'
        call_args = ['kotlinc', base_path + source_file_name + '.' + extension, '-include-runtime', '-d',
                     base_path + source_file_name + '.jar']
        popen_args = ['java', '-jar', base_path + source_file_name + compiled_file_extension]
    return compiled_file_extension, call_args, popen_args


def __check_test_for_task(source_code: str, in_file: str, out_file: str, task: str, extension='py',
                          source_file_name=SOURCE_FILE_NAME):
    compiled_file_extension = None
    if extension == 'java':
        source_file_name = __get_java_class(source_code)
    __create_source_code_file(source_code, task, extension, source_file_name)

    if extension == 'py':
        res = __run_python_test(in_file, __get_rows_from_file(out_file, task)[0], task)
    else:
        compiled_file_extension, call_args, popen_args = __get_args_for_run_programs(extension, task, source_file_name)
        res = __run_test(in_file, __get_rows_from_file(out_file, task)[0], task, call_args, popen_args)
    __drop_program_files(source_file_name,  extension, task, compiled_file_extension)
    return res


def __check_task(task: str, source_code: str, extension='py'):
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
        test_in = __get_test_in_file(cur_in, extension)
        count_tests += 1
        res = __check_test_for_task(source_code, test_in,
                                    out_files[__get_index_out_file_for_in_file(cur_in, out_files)], task, extension)
        if res:
            passed_tests += 1
    if extension == 'py':
        __drop_file(INPUT_FILE_NAME + '.' + extension, task)
    return count_tests, passed_tests


python_code_1 = 'a = int(input())\nb = int(input())\nn = int(input())\nprint(str(a * n) + " " + str((b * n)))'
java_code_1 = 'import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader(System.in);\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n        System.out.println(a * n + " " + b * n);\n    }\n}'
cpp_code_1 = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int a;\n    std::cin >> a;\n    int b;\n    std::cin >> b;\n    int n;\n    std::cin >> n;\n    cout << a * n << " " << b * n << endl;\n    return 0;\n}'
kotlin_code_1 = 'fun main(args: Array<String>) {\n    val a:Int = readLine()!!.toInt()\n    val b:Int = readLine()!!.toInt()\n    val n:Int = readLine()!!.toInt()\n    println((a * n).toString() + " " + (b * n).toString())\n}'
print(__check_task('pies', kotlin_code_1, extension='kt'))
