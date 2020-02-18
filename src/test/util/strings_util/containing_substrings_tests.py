import logging
import unittest

from main.util.consts import LOGGER_TEST_FILE
from main.util.strings_util import does_string_contain_any_of_substring

string = 'Roses are red, violets are blue, sugar is sweet, and so are you'
contained_substrings = ['red', 'blue']
partly_contained_substrings = ['mint', 'candy', 'sugar']
not_contained_substrings = ['parsley', 'sun']

class TestContainingSubstrings(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, level=logging.INFO)

    def test_contained_substrings(self):
        self.assertTrue(does_string_contain_any_of_substring(string, contained_substrings))

    def test_partly_contained_substrings(self):
        self.assertTrue(does_string_contain_any_of_substring(string, partly_contained_substrings))

    def test_not_contained_substrings(self):
        self.assertFalse(does_string_contain_any_of_substring(string, not_contained_substrings))

