# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.test.test_util import LoggedTest
from src.main.util.strings_util import contains_any_of_substrings

string = 'Roses are red, violets are blue, sugar is sweet, and so are you'
contained_substrings = ['red', 'blue']
partly_contained_substrings = ['mint', 'candy', 'sugar']
not_contained_substrings = ['parsley', 'sun']


class TestContainingSubstrings(LoggedTest):

    def test_contained_substrings(self) -> None:
        self.assertTrue(contains_any_of_substrings(string, contained_substrings))

    def test_partly_contained_substrings(self) -> None:
        self.assertTrue(contains_any_of_substrings(string, partly_contained_substrings))

    def test_not_contained_substrings(self) -> None:
        self.assertFalse(contains_any_of_substrings(string, not_contained_substrings))

