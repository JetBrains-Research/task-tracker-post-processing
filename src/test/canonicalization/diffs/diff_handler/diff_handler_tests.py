# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import re
import logging
import itertools
from random import randrange

from typing import List, Any, Optional, Tuple
from src.main.canonicalization.diffs.diff_handler import DiffHandler
from src.main.util.consts import LOGGER_NAME, TASK, EXTENSION
from src.main.util.file_util import get_content_from_file, get_all_file_system_items, match_condition, \
    get_name_from_path, change_extension_to, get_parent_folder
from src.test.canonicalization.util import run_test, DIFF_WORKER_TEST_TYPES, CANONIZATION_TESTS
from src.main.canonicalization.canonicalization import get_code_from_tree, get_cleaned_code
from src.test.test_util import LoggedTest

log = logging.getLogger(LOGGER_NAME)


DST_FOLDER = 'diff_handler'

OUT_FOR_RUN_STUDENTS_SOLUTION_TEST = {}

# (REVIEW) rename to FAILED_RUN_STUDENT..?
DOES_NOT_WORK_FOR_RUN_STUDENTS_SOLUTION_TEST = {
    TASK.BRACKETS: ['out_2_4.py', 'out_1_4.py'],
    TASK.ZERO: ['out_2_4.py'],
    TASK.PIES: ['out_3_1.py', 'out_2_3.py', 'out_2_1.py', 'out_2_3.py', 'out_2_4.py',
                'out_1_4.py', 'out_4_1.py'],
    TASK.ELECTION: ['out_1_3.py', 'out_1_2.py', 'out_1_5.py', 'out_1_4.py'],
    TASK.MAX_3: ['out_5_7.py', 'out_5_3.py', 'out_5_6.py', 'out_5_4.py'],
}


# (REVIEW): rename apply_diffs_between_files?
def apply_diffs(source_file: str, dst_source_file: Optional[str] = None) -> str:
    source = get_content_from_file(source_file)
    if not dst_source_file:
        dst_source_file = re.sub(r'in(?=[^in]*$)', 'out', source_file)

    dst_source = get_content_from_file(dst_source_file)

    src_diff_handler = DiffHandler(source)
    dst_diff_handler = DiffHandler(dst_source)

    diffs, tree_type = src_diff_handler.get_diffs_from_diff_handler(dst_diff_handler)
    res_tree = src_diff_handler.apply_diffs(diffs, tree_type)
    return get_code_from_tree(res_tree).rstrip('\n')


# (REVIEW) only 1 usage
def get_all_pairs(obj_list: List[Any]) -> List[Tuple[Any, Any]]:
    pairs = []
    for pair in itertools.product(obj_list, repeat=2):
        pairs.append(pair)
    return pairs


def get_files_by_reg_expr(test_type: DIFF_WORKER_TEST_TYPES, task: TASK, reg_expr: str) -> List[str]:
    root = os.path.join(CANONIZATION_TESTS.TASKS_TESTS_PATH.value, DST_FOLDER, test_type.value, task.value)
    return get_all_file_system_items(root, match_condition(reg_expr))


# (REVIEW) rename to src dst
def get_src_and_dst_files(test_type: DIFF_WORKER_TEST_TYPES, task: TASK) -> List[Tuple[Any, Any]]:
    in_files = get_files_by_reg_expr(test_type, task, r'\d+.py')
    return get_all_pairs(in_files)


# Todo: rename it
def get_out_file(src_file: str, dst_file: str) -> str:
    src_file_number = get_name_from_path(src_file, with_extension=False)
    dst_file_number = get_name_from_path(src_file, with_extension=False)
    return os.path.join(get_parent_folder(src_file), f'out{src_file_number}_{dst_file_number}.py')


class TestDiffWorker(LoggedTest):

    # def test_file_renaming(self):
    #     files = get_all_file_system_items('/home/elena/workspaces/python/codetracker-data/src/resources/test_data/canonicalization/canonicalization/diff_handler/students_code',
    #                                       match_condition(r'in_\d+.py'))
    #     for file in files:
    #         path = get_parent_folder(file, True)
    #         new_name = get_name_from_path(file)[3:]
    #         os.rename(file, path + new_name)

    # Find and apply all edits
    def test_diff_worker_with_all_edits(self) -> None:
        run_test(self, DIFF_WORKER_TEST_TYPES.DIFF_WORKER_TEST, apply_diffs,
                 additional_folder_name=DST_FOLDER,
                 to_clear_out=True)

    # Todo: still rename?
    def test_no_exceptions_raised_applying_diffs_to_students_code(self) -> None:
        for task in TASK:
            in_and_out_files = get_src_and_dst_files(DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, task)
            tests_count = 1
            for src_file, dst_file in in_and_out_files:
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
            in_and_out_files = get_src_and_dst_files(DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, task)
            count_tests = 1
            out_files = get_files_by_reg_expr(DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, task, r'out_\d+_\d+.py')
            for source_file, dst_file in in_and_out_files:
                log.info(f'Test number is {count_tests}\nSource file is: {source_file}\nGoal file is: {dst_file}\n')
                actual_out = apply_diffs(source_file, dst_file)

                out_file_name = get_out_file(source_file, dst_file)
                
                # Todo: delete it
                if get_name_from_path(out_file_name) in DOES_NOT_WORK_FOR_RUN_STUDENTS_SOLUTION_TEST.get(task, []):
                    continue

                if out_file_name in out_files:
                    out_file = os.path.join(get_parent_folder(source_file), out_file_name)
                    expected_out = get_cleaned_code(get_content_from_file(out_file)).rstrip('\n')
                else:
                    expected_out = get_cleaned_code(get_content_from_file(dst_file)).rstrip('\n')
                log.info(f'Actual code is:\n{actual_out}\nExpected code is:\n{expected_out}\n')
                self.assertEqual(expected_out, actual_out)
                count_tests += 1

