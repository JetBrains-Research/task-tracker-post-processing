# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import unittest

from .util import run_test
from src.main.util.consts import LOGGER_FORMAT, LOGGER_NAME, LOGGER_TEST_FILE, CANONIZATION_TESTS_TYPES, TASK
from src.main.util.file_util import get_content_from_file
from src.main.ast.canonicalization_tool import get_cleaned_code, anonymize_names, get_code_from_tree, get_ast, get_canonicalized_form

log = logging.getLogger(LOGGER_NAME)


def get_cleaned_code_from_file(file: str):
    source = get_content_from_file(file)
    return get_cleaned_code(source).rstrip('\n')


def get_code_with_anonymous_names(file: str):
    source = get_cleaned_code_from_file(file)
    tree = get_ast(source)
    actual_code = get_code_from_tree(anonymize_names(tree)).rstrip('\n')
    return actual_code


def get_canonicalized_code(file: str):
    source = get_content_from_file(file)
    return get_code_from_tree(get_canonicalized_form(source)).rstrip('\n')


class TestCanonicalizationTool(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_cleaned_code(self):
        run_test(self, CANONIZATION_TESTS_TYPES.CLEANED_CODE.value, get_cleaned_code_from_file)

    def test_anonymize_names(self):
        run_test(self, CANONIZATION_TESTS_TYPES.ANONYMIZE_NAMES.value, get_code_with_anonymous_names)

    def test_canonical_form(self):
        run_test(self, CANONIZATION_TESTS_TYPES.CANONICAL_FORM.value, get_canonicalized_code)

    def test_student_code_pies(self):
        run_test(self, CANONIZATION_TESTS_TYPES.STUDENT_CODE.value, get_canonicalized_code, TASK.PIES.value)

    def test_student_code_max_3(self):
        run_test(self, CANONIZATION_TESTS_TYPES.STUDENT_CODE.value, get_canonicalized_code, TASK.MAX_3.value)

    def test_student_code_is_zero(self):
        run_test(self, CANONIZATION_TESTS_TYPES.STUDENT_CODE.value, get_canonicalized_code, TASK.ZERO.value)

    def test_student_code_max_digit(self):
        run_test(self, CANONIZATION_TESTS_TYPES.STUDENT_CODE.value, get_canonicalized_code, TASK.MAX_DIGIT.value)

    def test_student_code_election(self):
        run_test(self, CANONIZATION_TESTS_TYPES.STUDENT_CODE.value, get_canonicalized_code, TASK.ELECTION.value)

    def test_student_code_brackets(self):
        run_test(self, CANONIZATION_TESTS_TYPES.STUDENT_CODE.value, get_canonicalized_code, TASK.BRACKETS.value)
