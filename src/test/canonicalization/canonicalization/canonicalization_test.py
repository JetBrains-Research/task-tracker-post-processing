# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Callable, Tuple, Optional

import pytest

from src.main.util.consts import LOGGER_NAME, TASK
from src.test.test_config import to_skip, TEST_LEVEL
from src.main.canonicalization.consts import TREE_TYPE
from src.main.util.file_util import get_content_from_file
from src.test.canonicalization.diffs.diff_handler.util import FAIL_REASON
from src.test.canonicalization.util import run_test, CANONICALIZATION_TESTS_TYPES
from src.main.canonicalization.canonicalization import get_cleaned_code, get_code_from_tree, get_trees

log = logging.getLogger(LOGGER_NAME)

ADDITIONAL_FOLDER = 'canonicalization'


def get_cleaned_code_from_file(file: str) -> str:
    source = get_content_from_file(file)
    return get_cleaned_code(source).rstrip('\n')


def get_anonymized_code_from_file(file: str) -> str:
    anon_tree, = get_trees(get_content_from_file(file), {TREE_TYPE.ANON}, False)
    return get_code_from_tree(anon_tree).rstrip('\n')


def get_canonicalized_code_from_file(file: str) -> str:
    canon_tree, = get_trees(get_content_from_file(file), {TREE_TYPE.CANON})
    return get_code_from_tree(canon_tree).rstrip('\n')


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.CANONICALIZATION),
                    reason=TEST_LEVEL.CANONICALIZATION.value)
@pytest.mark.xfail(reason=FAIL_REASON)
class TestCanonicalizationTool:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (CANONICALIZATION_TESTS_TYPES.CLEANED_CODE, get_cleaned_code_from_file, None),
                        (CANONICALIZATION_TESTS_TYPES.ANONYMIZE_NAMES, get_anonymized_code_from_file, None),
                        (CANONICALIZATION_TESTS_TYPES.CANONICAL_FORM, get_canonicalized_code_from_file, None),
                        (CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.PIES),
                        (CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.MAX_3),
                        (CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.ZERO),
                        (CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.MAX_DIGIT),
                        (CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.VOTING),
                        (CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.BRACKETS),
                    ],
                    ids=[
                        'test_cleaned_code',
                        'test_anonymize_names',
                        'test_canonical_form',
                        'test_student_code_pies',
                        'test_student_code_max_3',
                        'test_student_code_is_zero',
                        'test_student_code_max_digit',
                        'test_student_code_election',
                        'test_student_code_brackets'
                    ]
                    )
    def param_canonicalization_tool_test(request) -> Tuple[CANONICALIZATION_TESTS_TYPES, Callable, Optional[TASK]]:
        return request.param

    def test_canonicalization_tool(self, param_canonicalization_tool_test: Callable) -> None:
        (test_type, get_code_function, task) = param_canonicalization_tool_test
        run_test(test_type, get_code_function, task=task, additional_folder_name=ADDITIONAL_FOLDER)
