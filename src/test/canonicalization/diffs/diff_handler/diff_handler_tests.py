import os
import re
import logging
import unittest
import itertools

from typing import List, Any, Optional, Tuple

from src.main.canonicalization.consts import TREE_TYPE
from src.main.canonicalization.diffs.diff_handler import DiffHandler
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT, LOGGER_NAME, TASK, EXTENSION
from src.main.util.file_util import get_content_from_file, get_all_file_system_items, match_condition, \
    get_name_from_path, change_extension_to, get_parent_folder
from src.test.canonicalization.util import run_test, DIFF_WORKER_TEST_TYPES, CANONIZATION_TESTS
from src.main.canonicalization.canonicalization import get_code_from_tree, get_cleaned_code, get_trees


log = logging.getLogger(LOGGER_NAME)


DST_FOLDER = 'diff_handler'

OUT_FOR_RUN_STUDENTS_SOLUTION_TEST = {}

DOES_NOT_WORK_FOR_RUN_STUDENTS_SOLUTION_TEST = {
    TASK.BRACKETS: ['out_2_4.py', 'out_1_4.py'],
    TASK.ZERO: ['out_2_4.py'],
    TASK.PIES: ['out_3_1.py', 'out_2_3.py', 'out_2_1.py', 'out_2_3.py', 'out_2_4.py',
                'out_1_4.py', 'out_4_1.py'],
    TASK.ELECTION: ['out_1_3.py', 'out_1_2.py', 'out_1_5.py', 'out_1_4.py'],
    TASK.MAX_3: ['out_5_7.py', 'out_5_3.py', 'out_5_6.py', 'out_5_4.py'],
}


def apply_diffs(src_file: str, dst_file: str) -> str:
    src_diff_handler = DiffHandler(get_content_from_file(src_file))
    dst_diff_handler = DiffHandler(get_content_from_file(dst_file))
    diffs, tree_type = src_diff_handler.get_diffs_from_diff_handler(dst_diff_handler)
    res_tree = src_diff_handler.apply_diffs(diffs, tree_type)
    return get_code_from_tree(res_tree).rstrip('\n')


def get_files_by_reg_expr(test_type: DIFF_WORKER_TEST_TYPES, task: TASK, reg_expr: str) -> List[str]:
    root = os.path.join(CANONIZATION_TESTS.TASKS_TESTS_PATH.value, DST_FOLDER, test_type.value, task.value)
    return get_all_file_system_items(root, match_condition(reg_expr))


def get_src_and_dst_files(test_type: DIFF_WORKER_TEST_TYPES, task: TASK) -> List[Tuple[str, str]]:
    files = get_files_by_reg_expr(test_type, task, r'\d+.py')
    return list(itertools.product(files, repeat=2))


def get_in_and_out_files(test_type: DIFF_WORKER_TEST_TYPES, task: TASK) -> List[Tuple[str, str, str]]:
    src_and_dst_files = get_src_and_dst_files(test_type, task)
    in_and_out_files = []
    for src_file, dst_file in src_and_dst_files:
        src_file_number = get_name_from_path(src_file, with_extension=False)
        dst_file_number = get_name_from_path(dst_file, with_extension=False)
        out_file = os.path.join(get_parent_folder(src_file), f'out_{src_file_number}_{dst_file_number}.py')

        if get_name_from_path(out_file) in DOES_NOT_WORK_FOR_RUN_STUDENTS_SOLUTION_TEST.get(task, []):
            continue

        # If there is no such out_file, it means that out code is the same as dst code from dst_file
        if not os.path.isfile(out_file):
            out_file = dst_file

        if get_name_from_path(out_file) in DOES_NOT_WORK_FOR_RUN_STUDENTS_SOLUTION_TEST.get(task, []):
            continue

        in_and_out_files.append((src_file, dst_file, out_file))
        # in_and_out_files.append((get_name_from_path(src_file), get_name_from_path(dst_file), get_name_from_path(out_file)))
    return in_and_out_files



# Todo: rename it
def get_out_file(source_file: str, dst_file: str) -> str:
    src_file_number = get_name_from_path(source_file, with_extension=False)
    dst_file_number = get_name_from_path(dst_file, with_extension=False)
    return os.path.join(get_parent_folder(source_file), f'out_{src_file_number}_{dst_file_number}.py')


class TestDiffWorker(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    # def test_rename(self):
    #     files = get_all_file_system_items('/home/elena/workspaces/python/codetracker-data/src/resources/test_data/canonicalization/canonicalization/diff_handler/students_code/',
    #                                       match_condition(r'in_\d+.py'))
    #     for file in files:
    #         path = get_parent_folder(file, True)
    #         name = get_name_from_path(file)
    #         new_name = name[3:]
    #         os.rename(file, path + new_name)
    #
    #         print(file)

    # Find and apply all edits
    def test_diff_worker_with_all_edits(self) -> None:
        run_test(self, DIFF_WORKER_TEST_TYPES.DIFF_WORKER_TEST, apply_diffs,
                 additional_folder_name=DST_FOLDER,
                 to_clear_out=True)

    def test_no_exceptions_raised_applying_diffs_to_students_code(self) -> None:
        for task in TASK:
            srs_and_dst_files = get_src_and_dst_files(DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, task)
            tests_count = 1
            for src_file, dst_file in srs_and_dst_files:
                test_info = f'Task {task.value}\nTest number {tests_count}\nSrc file is: {src_file}\nDst file is: {dst_file}\n'
                log.info(test_info)
                with self.subTest():
                    try:
                        apply_diffs(src_file, dst_file)
                    except Exception as e:
                        self.fail(f'Exception {e} was raised\n{test_info}')
                tests_count += 1

    def test_result_of_applying_diffs_to_students_code(self) -> None:
        for task in TASK:
            tests_count = 1
            in_and_out_files = get_in_and_out_files(DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, task)
            for src_file, dst_file, out_file in in_and_out_files:
                test_info = f'Task {task.value}\nTest number {tests_count}\nSrc file is: {src_file}\nDst file is: {dst_file}\n'
                log.info(test_info)
                with self.subTest():
                    actual_out = apply_diffs(src_file, dst_file)
                    expected_out = get_cleaned_code(get_content_from_file(out_file)).rstrip('\n')
                    log.info(f'Actual code is:\n{actual_out}\nExpected code is:\n{expected_out}\n')
                    self.assertEqual(expected_out, actual_out, test_info)
                tests_count += 1

