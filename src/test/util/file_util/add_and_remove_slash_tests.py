import logging
import unittest

from main.util.consts import LOGGER_TEST_FILE
from main.util.file_util import add_slash, remove_slash

path_with_slash = 'home/data/src/'
path_without_slash = 'home/data/src'
empty_path_without_slash = ''
empty_path_with_slash = '/'


class TestAddAndRemoveSlash(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, level=logging.INFO)

    def test_add_not_existing_slash(self):
        path_with_added_slash = add_slash(path_without_slash)
        self.assertTrue(path_with_added_slash == path_with_slash)

    def test_add_existing_slash(self):
        path_with_added_slash = add_slash(path_with_slash)
        self.assertTrue(path_with_added_slash == path_with_slash)

    def test_add_not_existing_slash_to_empty_slash(self):
        empty_path_with_added_slash = add_slash(empty_path_without_slash)
        self.assertTrue(empty_path_with_added_slash == empty_path_with_slash)

    def test_add_existing_slash_to_empty_slash(self):
        empty_path_with_added_slash = add_slash(empty_path_with_slash)
        self.assertTrue(empty_path_with_added_slash == empty_path_with_slash)

    def test_remove_not_existing_slash(self):
        path_with_removed_slash = remove_slash(path_without_slash)
        self.assertTrue(path_with_removed_slash == path_without_slash)

    def test_remove_existing_slash(self):
        path_with_removed_slash = remove_slash(path_with_slash)
        self.assertTrue(path_with_removed_slash == path_without_slash)

    def test_remove_not_existing_slash_from_empty_slash(self):
        empty_path_with_removed_slash = remove_slash(empty_path_without_slash)
        self.assertTrue(empty_path_with_removed_slash == empty_path_without_slash)

    def test_remove_existing_slash_from_empty_slash(self):
        empty_path_with_removed_slash = remove_slash(empty_path_with_slash)
        self.assertTrue(empty_path_with_removed_slash == empty_path_without_slash)
