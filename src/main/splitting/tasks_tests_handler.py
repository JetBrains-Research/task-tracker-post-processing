import os
import re
import logging

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.splitting.task_checker import TASKS_TESTS_PATH
from src.main.util.file_util import get_all_file_system_items
from src.main.splitting.cpp_task_checker import CppTaskChecker
from src.main.splitting.java_task_checker import JavaTaskChecker
from src.main.splitting.kotlin_task_checker import KotlinTaskChecker
from src.main.splitting.python_task_checker import PythonTaskChecker
from src.main.splitting.not_defined_task_checker import NotDefinedTaskChecker

log = logging.getLogger(consts.LOGGER_NAME)


def __pair_up_in_and_out_files(in_files: list, out_files: list):
    pairs = []
    for in_file in in_files:
        out_file = re.sub(r'in(?=[^in]*$)', 'out', in_file)
        if out_file not in out_files:
            raise ValueError(f'List of out files does not contain a file for {in_file}')
        pairs.append((in_file, out_file))
    return pairs


def create_in_and_out_dict(tasks: list):
    in_and_out_files_dict = {}
    for task in tasks:
        root = os.path.join(TASKS_TESTS_PATH, task)
        in_files = get_all_file_system_items(root, (lambda filename: re.fullmatch(r'in_\d+.txt', filename)))
        out_files = get_all_file_system_items(root, (lambda filename: re.fullmatch(r'out_\d+.txt', filename)))
        if len(out_files) != len(in_files):
            raise ValueError('Length of out files list does not equal in files list')
        in_and_out_files_dict[task] = __pair_up_in_and_out_files(in_files, out_files)
    return in_and_out_files_dict


def check_tasks(tasks: list, source_code: str, in_and_out_files_dict: dict, language=LANGUAGE.PYTHON.value, stop_after_first_false=True):
    if language == LANGUAGE.PYTHON.value:
        task_checker = PythonTaskChecker()
    elif language == LANGUAGE.JAVA.value:
        task_checker = JavaTaskChecker()
    elif language == LANGUAGE.CPP.value:
        task_checker = CppTaskChecker()
    elif language == LANGUAGE.KOTLIN.value:
        task_checker = KotlinTaskChecker()
    else:
        task_checker = NotDefinedTaskChecker()

    return task_checker.check_tasks(tasks, source_code, in_and_out_files_dict, stop_after_first_false)
