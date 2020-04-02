import os
import re
import logging
import unittest
import itertools

from typing import List, Any, Optional, Tuple
from src.main.canonicalization.diffs.diff_worker import DiffWorker
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT, LOGGER_NAME, TASK, EXTENSION
from src.main.util.file_util import get_content_from_file, get_all_file_system_items, match_condition, \
    get_name_from_path, change_extension_to, get_parent_folder
from src.test.canonicalization.util import run_test, DIFF_WORKER_TEST_TYPES, CANONIZATION_TESTS
from src.main.canonicalization.canonicalization import get_code_from_tree, get_canonicalized_and_orig_form, \
    get_canonicalized_form, get_cleaned_code

log = logging.getLogger(LOGGER_NAME)


DST_FOLDER = 'diff_worker'

OUT_FOR_RUN_STUDENTS_SOLUTION_TEST = {}

DOES_NOT_WORK_FOR_RUN_STUDENTS_SOLUTION_TEST = {
    TASK.BRACKETS: ['out_2_4.py', 'out_1_4.py'],
    TASK.ZERO: ['out_2_4.py'],
    TASK.PIES: ['out_3_1.py', 'out_2_3.py', 'out_2_1.py', 'out_2_3.py', 'out_2_4.py',
                'out_1_4.py', 'out_4_1.py']
}


def apply_diffs(source_file: str, dst_source_file: Optional[str] = None) -> str:
    source = get_content_from_file(source_file)
    if not dst_source_file:
        dst_source_file = re.sub(r'in(?=[^in]*$)', 'out', source_file)

    dst_source = get_content_from_file(dst_source_file)

    anon_dst_tree, orig_dst_tree = get_canonicalized_and_orig_form(dst_source, only_anon=True)
    canon_dst_tree = get_canonicalized_form(anon_dst_tree)

    diff_worker = DiffWorker(source)
    edits, tree_type = diff_worker.get_diffs(anon_dst_tree, canon_dst_tree)
    res_tree = diff_worker.apply_diffs(edits, tree_type)
    return get_code_from_tree(res_tree).rstrip('\n')


def get_all_pairs(obj_list: List[Any]) -> List[Tuple[Any, Any]]:
    pairs = []
    for pair in itertools.product(obj_list, repeat=2):
        pairs.append(pair)
    return pairs


def __get_files_by_reg_expr(test_type: DIFF_WORKER_TEST_TYPES, task: TASK, reg_expr: str) -> List[str]:
    root = os.path.join(CANONIZATION_TESTS.TASKS_TESTS_PATH.value, DST_FOLDER, test_type.value, task.value)
    return get_all_file_system_items(root, match_condition(reg_expr))


def get_in_and_out_files(test_type: DIFF_WORKER_TEST_TYPES, task: TASK) -> List[Tuple[Any, Any]]:
    in_files = __get_files_by_reg_expr(test_type, task, r'in_\d+.py')
    return get_all_pairs(in_files)


# Todo: rename it
# Test if the functions get edits and apply diffs work
def run_students_solution_apply_diffs_test(self, test_type: DIFF_WORKER_TEST_TYPES, task: TASK) -> None:
    in_and_out_files = get_in_and_out_files(test_type, task)
    count_tests = 1
    for source_file, dst_file in in_and_out_files:
        log.info(f'Test number is {count_tests}\nSource file is: {source_file}\nGoal file is: {dst_file}\n')
        actual_out = apply_diffs(source_file, dst_file)
        log.info(f'Actual code is:\n{actual_out}\nExpected code is:\n{actual_out}\n')
        self.assertTrue(True)
        count_tests += 1


def __init_out_dict(test_type: DIFF_WORKER_TEST_TYPES, task: TASK) -> None:
    OUT_FOR_RUN_STUDENTS_SOLUTION_TEST[task] = __get_files_by_reg_expr(test_type, task, r'out_\d+_\d+.py')


def __is_contain_out_for_run_students_solution_test(task: TASK, out_file: str) -> bool:
    return out_file in OUT_FOR_RUN_STUDENTS_SOLUTION_TEST.get(task, [])


# Todo: rename it
def __get_out_file(source_file: str, dst_file: str) -> str:
    source_file_name = change_extension_to(get_name_from_path(source_file), EXTENSION.EMPTY)
    dst_file_name = get_name_from_path(dst_file)
    source_number = re.sub(r'in(?=[^in]*$)', '', source_file_name)
    dst_number_with_extenstion = re.sub(r'in(?=[^in]*$)', '', dst_file_name)
    return os.path.join(get_parent_folder(source_file), 'out' + source_number + dst_number_with_extenstion)


# Todo: rename it and thinking about it
def run_students_solution_test(self, test_type: DIFF_WORKER_TEST_TYPES, task: TASK) -> None:
    in_and_out_files = get_in_and_out_files(test_type, task)
    count_tests = 1
    __init_out_dict(test_type, task)
    for source_file, dst_file in in_and_out_files:
        log.info(f'Test number is {count_tests}\nSource file is: {source_file}\nGoal file is: {dst_file}\n')
        actual_out = apply_diffs(source_file, dst_file)

        out_file_name = __get_out_file(source_file, dst_file)
        # Todo: delete it
        if get_name_from_path(out_file_name) in DOES_NOT_WORK_FOR_RUN_STUDENTS_SOLUTION_TEST.get(task, []):
            continue

        if __is_contain_out_for_run_students_solution_test(task, out_file_name):
            out_file = os.path.join(get_parent_folder(source_file), out_file_name)
            expected_out = get_cleaned_code(get_content_from_file(out_file)).rstrip('\n')
        else:
            expected_out = get_cleaned_code(get_content_from_file(dst_file)).rstrip('\n')
        log.info(f'Actual code is:\n{actual_out}\nExpected code is:\n{expected_out}\n')
        self.assertEqual(expected_out, actual_out)
        count_tests += 1


class TestDiffWorker(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    # Find and apply all edits
    def test_diff_worker_with_all_edits(self) -> None:
        run_test(self, DIFF_WORKER_TEST_TYPES.DIFF_WORKER_TEST, apply_diffs,
                 additional_folder_name=DST_FOLDER,
                 to_clear_out=True)

    def test_running_brackets_students_solution(self) -> None:
        run_students_solution_apply_diffs_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.BRACKETS)

    def test_running_is_zero_students_solution(self) -> None:
        run_students_solution_apply_diffs_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.ZERO)

    def test_running_max_digit_students_solution(self) -> None:
        run_students_solution_apply_diffs_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.MAX_DIGIT)

    def test_running_pies_students_solution(self) -> None:
        run_students_solution_apply_diffs_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.PIES)

    def test_running_election_students_solution(self) -> None:
        run_students_solution_apply_diffs_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.ELECTION)

    def test_running_max_3_students_solution(self) -> None:
        run_students_solution_apply_diffs_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.MAX_3)

    def test_brackets_students_solution(self) -> None:
        run_students_solution_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.BRACKETS)

    def test_is_zero_students_solution(self) -> None:
        run_students_solution_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.ZERO)

    def test_max_digit_students_solution(self) -> None:
        run_students_solution_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.MAX_DIGIT)

    def test_pies_students_solution(self) -> None:
        run_students_solution_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.PIES)

    # def test_election_students_solution(self) -> None:
    #     run_students_solution_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.ELECTION)
