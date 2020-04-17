# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import re
import pytest
import logging
import itertools
from typing import List, Optional, Tuple


from src.test.util import does_skip, TEST_LEVEL
from src.main.util.consts import LOGGER_NAME, TASK
from src.main.util.log_util import log_and_raise_error
from src.main.canonicalization.diffs.diff_handler import DiffHandler
from src.main.canonicalization.canonicalization import get_code_from_tree, get_cleaned_code
from src.test.canonicalization.util import run_test, DIFF_HANDLER_TEST_TYPES, CANONICALIZATION_TESTS
from src.main.util.file_util import get_content_from_file, get_name_from_path, match_condition, get_parent_folder, \
     get_all_file_system_items

log = logging.getLogger(LOGGER_NAME)

ADDITIONAL_FOLDER = 'diffs/diff_handler'

FAILED_APPLYING_DIFFS_TO_STUDENTS_CODE_TEST = {
    TASK.BRACKETS: ['out_2_4.py', 'out_1_4.py'],
    TASK.ZERO: ['out_2_4.py'],
    TASK.PIES: ['out_3_1.py', 'out_2_3.py', 'out_2_1.py', 'out_2_3.py', 'out_2_4.py',
                'out_1_4.py', 'out_4_1.py'],
    TASK.ELECTION: ['out_1_3.py', 'out_1_2.py', 'out_1_5.py', 'out_1_4.py'],
    TASK.MAX_3: ['out_5_7.py', 'out_5_3.py', 'out_5_6.py', 'out_5_4.py'],
}


def apply_diffs(src_file: str, dst_file: Optional[str] = None) -> str:
    if not dst_file:
        dst_file = re.sub(r'in(?=[^in]*$)', 'out', src_file)
    src_diff_handler = DiffHandler(get_content_from_file(src_file))
    dst_diff_handler = DiffHandler(get_content_from_file(dst_file))
    diffs, tree_type = src_diff_handler.get_diffs_from_diff_handler(dst_diff_handler)
    res_tree = src_diff_handler.apply_diffs(diffs, tree_type)
    return get_code_from_tree(res_tree).rstrip('\n')


def get_src_and_dst_files(test_type: DIFF_HANDLER_TEST_TYPES, task: TASK) -> List[Tuple[str, str]]:
    root = os.path.join(CANONICALIZATION_TESTS.DATA_PATH.value, ADDITIONAL_FOLDER, test_type.value, task.value)
    files = get_all_file_system_items(root, match_condition(r'\d+.py'))
    if len(files) == 0:
        log_and_raise_error(f'Number of test files is zero! Root for files is {root}', log)
    return list(itertools.product(files, repeat=2))


# For applying diffs we need to have src_file and dst_file. In theory, we should compare the code after
# applying diffs with dst-code, but sometimes we get a different code that is still correct (for example, has
# different variables names). In that case we have an additional out_file to compare with. So, we have:
# 'in'-files: src (i.py) and dst (j.py) files
# 'out'-files: out_i_j.py if exists, skipped if it's in FAILED_APPLYING_DIFFS_TO_STUDENTS_CODE_TEST and j.py otherwise
def get_in_and_out_files(test_type: DIFF_HANDLER_TEST_TYPES, task: TASK) -> List[Tuple[str, str, str]]:
    src_and_dst_files = get_src_and_dst_files(test_type, task)
    in_and_out_files = []
    for src_file, dst_file in src_and_dst_files:
        src_file_number = get_name_from_path(src_file, with_extension=False)
        dst_file_number = get_name_from_path(dst_file, with_extension=False)
        out_file = os.path.join(get_parent_folder(src_file), f'out_{src_file_number}_{dst_file_number}.py')
        if get_name_from_path(out_file) in FAILED_APPLYING_DIFFS_TO_STUDENTS_CODE_TEST.get(task, []):
            continue
        # If there is no such out_file, it means that out-code is the same as dst-code from dst_file
        if not os.path.isfile(out_file):
            out_file = dst_file
        in_and_out_files.append((src_file, dst_file, out_file))
    return in_and_out_files


@pytest.mark.skipif(does_skip(current_module_level=TEST_LEVEL.CANONICALIZATION),
                    reason=TEST_LEVEL.CANONICALIZATION.value)
class TestDiffHandler:

    # Find and apply all diffs
    def test_diff_worker_with_all_edits(self) -> None:
        run_test(DIFF_HANDLER_TEST_TYPES.DIFF_HANDLER_TEST, apply_diffs, additional_folder_name=ADDITIONAL_FOLDER,
                 to_clear_out=True)

    @pytest.mark.parametrize('task', [task for task in TASK])
    def test_no_exceptions_raised_applying_diffs_to_students_code(self, task) -> None:
        srs_and_dst_files = get_src_and_dst_files(DIFF_HANDLER_TEST_TYPES.STUDENTS_CODE, task)

        # Todo: add parametrize
        for i, (src_file, dst_file) in enumerate(srs_and_dst_files):
            test_info = f'Task {task.value}\nTest number {i}\nSrc file is: {src_file}\n' \
                        f'Dst file is: {dst_file}\n'
            log.info(test_info)
            try:
                apply_diffs(src_file, dst_file)
            except Exception as e:
                pytest.fail(f'Exception {e} was raised\n{test_info}')

    @pytest.mark.parametrize('task', [task for task in TASK])
    def test_result_of_applying_diffs_to_students_code(self, task) -> None:
        in_and_out_files = get_in_and_out_files(DIFF_HANDLER_TEST_TYPES.STUDENTS_CODE, task)
        # Todo: add parametrize
        for i, (src_file, dst_file, out_file) in enumerate(in_and_out_files):
            test_info = f'Task {task.value}\nTest number {i}\nSrc file is: {src_file}\n' \
                        f'Dst file is: {dst_file}\n'
            log.info(test_info)

            actual_out = apply_diffs(src_file, dst_file)
            expected_out = get_cleaned_code(get_content_from_file(out_file)).rstrip('\n')
            log.info(f'Actual code is:\n{actual_out}\nExpected code is:\n{expected_out}\n')
            assert expected_out == actual_out, test_info
