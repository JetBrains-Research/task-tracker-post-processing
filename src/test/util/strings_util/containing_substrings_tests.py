# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import unittest

from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT
from src.main.util.strings_util import contains_any_of_substrings

string = 'Roses are red, violets are blue, sugar is sweet, and so are you'
contained_substrings = ['red', 'blue']
partly_contained_substrings = ['mint', 'candy', 'sugar']
not_contained_substrings = ['parsley', 'sun']


class TestContainingSubstrings(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_contained_substrings(self):
        self.assertTrue(contains_any_of_substrings(string, contained_substrings))

    def test_partly_contained_substrings(self):
        self.assertTrue(contains_any_of_substrings(string, partly_contained_substrings))

    def test_not_contained_substrings(self):
        self.assertFalse(contains_any_of_substrings(string, not_contained_substrings))

