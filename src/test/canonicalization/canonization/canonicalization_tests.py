# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import unittest

from src.test.canonicalization.canonization.util import run_test, CANONIZATION_TESTS_TYPES
from src.main.util.file_util import get_content_from_file
from src.main.util.consts import LOGGER_FORMAT, LOGGER_NAME, LOGGER_TEST_FILE
from src.main.canonicalization.canonicalization import get_cleaned_code, anonymize_names, print_tree, get_ast, get_canonical_form

log = logging.getLogger(LOGGER_NAME)


def get_actual_cleaned_code(file: str):
    source = get_content_from_file(file)
    return get_cleaned_code(source).rstrip('\n')


def get_code_with_anonymous_names(file: str):
    source = get_actual_cleaned_code(file)
    tree = get_ast(source)
    actual_code = print_tree(anonymize_names(tree)).rstrip('\n')
    return actual_code


def get_canonical_code(file: str):
    source = get_content_from_file(file)
    anon_tree = get_ast(get_cleaned_code(source).rstrip('\n'))
    canonical_form = get_canonical_form(anon_tree)
    actual_code = print_tree(anonymize_names(canonical_form)).rstrip('\n')
    return actual_code


class TestCanonicalizationTool(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_cleaned_code(self):
        run_test(self, CANONIZATION_TESTS_TYPES.CLEANED_CODE.value, get_actual_cleaned_code)

    def test_anonymize_names(self):
        run_test(self, CANONIZATION_TESTS_TYPES.ANONYMIZE_NAMES.value, get_code_with_anonymous_names)

    def test_canonical_form(self):
        run_test(self, CANONIZATION_TESTS_TYPES.CANONICAL_FORM.value, get_canonical_code)
