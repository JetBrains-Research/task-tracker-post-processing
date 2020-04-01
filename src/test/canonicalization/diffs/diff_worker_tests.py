import os
import re
import logging
import unittest
import itertools

from typing import List, Any, Optional, Tuple
from src.main.canonicalization.diffs.diff_worker import DiffWorker
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT, LOGGER_NAME, TASK
from src.main.util.file_util import get_content_from_file, get_all_file_system_items
from src.test.canonicalization.util import run_test, DIFF_WORKER_TEST_TYPES, CANONIZATION_TESTS
from src.main.canonicalization.canonicalization import get_code_from_tree, get_canonicalized_and_orig_form, \
    get_canonicalized_form

log = logging.getLogger(LOGGER_NAME)


DST_FOLDER = 'diff_worker'


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


def get_in_and_out_files(test_type: DIFF_WORKER_TEST_TYPES, task: TASK) -> List[Tuple[Any, Any]]:
    root = os.path.join(CANONIZATION_TESTS.TASKS_TESTS_PATH.value, DST_FOLDER, test_type.value, task.value)
    in_files = get_all_file_system_items(root, (lambda filename: re.fullmatch(r'in_\d+.py', filename)))
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


# Todo: rename it and thinking about it
def run_students_solution_test(self, test_type: DIFF_WORKER_TEST_TYPES, task: TASK) -> None:
    in_and_out_files = get_in_and_out_files(test_type, task)
    count_tests = 1
    for source_file, dst_file in in_and_out_files:
        log.info(f'Test number is {count_tests}\nSource file is: {source_file}\nGoal file is: {dst_file}\n')
        actual_out_tree, _ = get_canonicalized_and_orig_form(apply_diffs(source_file, dst_file))
        actual_out = get_code_from_tree(actual_out_tree).rstrip('\n')
        expected_out_tree, _ = get_canonicalized_and_orig_form(get_content_from_file(dst_file))
        expected_out = get_code_from_tree(expected_out_tree).rstrip('\n')
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

    # def test_brackets_students_solution(self) -> None:
    #     run_students_solution_test(self, DIFF_WORKER_TEST_TYPES.STUDENTS_CODE, TASK.BRACKETS)
