# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

from src.test.test_util import LoggedTest
from src.main.util.consts import LOGGER_NAME, TASK
from src.main.canonicalization.consts import TREE_TYPE
from src.main.util.file_util import get_content_from_file
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


class TestCanonicalizationTool(LoggedTest):

    def test_cleaned_code(self) -> None:
        run_test(self, CANONICALIZATION_TESTS_TYPES.CLEANED_CODE, get_cleaned_code_from_file,
                 additional_folder_name=ADDITIONAL_FOLDER)

    # Todo: there are no files for this test, is it ok?
    def test_anonymize_names(self) -> None:
        run_test(self, CANONICALIZATION_TESTS_TYPES.ANONYMIZE_NAMES, get_anonymized_code_from_file,
                 additional_folder_name=ADDITIONAL_FOLDER)

    def test_canonical_form(self) -> None:
        run_test(self, CANONICALIZATION_TESTS_TYPES.CANONICAL_FORM, get_canonicalized_code_from_file,
                 additional_folder_name=ADDITIONAL_FOLDER)

    def test_student_code_pies(self) -> None:
        run_test(self, CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.PIES,
                 additional_folder_name=ADDITIONAL_FOLDER)

    def test_student_code_max_3(self) -> None:
        run_test(self, CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.MAX_3,
                 additional_folder_name=ADDITIONAL_FOLDER)

    def test_student_code_is_zero(self) -> None:
        run_test(self, CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.ZERO,
                 additional_folder_name=ADDITIONAL_FOLDER)

    def test_student_code_max_digit(self) -> None:
        run_test(self, CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.MAX_DIGIT,
                 additional_folder_name=ADDITIONAL_FOLDER)

    def test_student_code_election(self) -> None:
        run_test(self, CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.ELECTION,
                 additional_folder_name=ADDITIONAL_FOLDER)

    def test_student_code_brackets(self) -> None:
        run_test(self, CANONICALIZATION_TESTS_TYPES.STUDENT_CODE, get_canonicalized_code_from_file, TASK.BRACKETS,
                 additional_folder_name=ADDITIONAL_FOLDER)
