import logging
import os
import unittest

from main.util.consts import LOGGER_TEST_FILE, TEST_DATA_PATH
from main.util.file_util import get_extension_from_file, change_extension_to, create_file, remove_file, \
    remove_directory, create_directory, add_dot_to_not_empty_extension

# Assuming there cannot be any slashes at the end of the file, because path 'home/data/file.txt/ is incorrect
file_with_txt_extension = os.path.join(TEST_DATA_PATH, 'util/file_util/extension_tests/file.txt')
file_with_csv_extension = os.path.join(TEST_DATA_PATH, 'util/file_util/extension_tests/file.csv')
file_without_extension = os.path.join(TEST_DATA_PATH, 'util/file_util/extension_tests/file')
folder_with_slash = os.path.join(TEST_DATA_PATH, 'util/file_util/extension_tests/')

extension_with_dot = '.txt'
extension_without_dot = 'txt'
empty_extension = ''


def clear_folder(folder):
    remove_directory(folder)
    create_directory(folder)


class TestExtensionMethods(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, level=logging.INFO)

    def test_getting_txt_extension(self):
        self.assertTrue('.txt' == get_extension_from_file(file_with_txt_extension))

    def test_getting_empty_extension(self):
        self.assertTrue('' == get_extension_from_file(file_without_extension))

    def test_getting_exception_from_folder(self):
        self.assertTrue('' == get_extension_from_file(folder_with_slash))

    # for testing extension change we should use real files
    def test_changing_extension(self):
        clear_folder(folder_with_slash)
        create_file("", '.csv', file_without_extension,)
        change_extension_to(file_with_csv_extension, '.txt')
        self.assertTrue(os.path.isfile(file_with_txt_extension))
        remove_file(file_with_txt_extension)

    def test_changing_to_empty_extension(self):
        clear_folder(folder_with_slash)
        create_file("", '.csv', file_without_extension,)
        change_extension_to(file_with_csv_extension, '')
        self.assertTrue(os.path.isfile(file_without_extension))
        remove_file(file_without_extension)

    def test_changing_empty_extension(self):
        clear_folder(folder_with_slash)
        create_file("", '', file_without_extension, )
        change_extension_to(file_without_extension, '.txt')
        self.assertTrue(os.path.isfile(file_with_txt_extension))
        remove_file(file_with_txt_extension)

    def test_adding_dot_to_extension_with_dot(self):
        self.assertTrue(extension_with_dot == add_dot_to_not_empty_extension(extension_with_dot))

    def test_adding_dot_to_extension_without_dot(self):
        self.assertTrue(extension_with_dot == add_dot_to_not_empty_extension(extension_without_dot))

    def test_adding_dot_to_empty_extension(self):
        self.assertTrue(empty_extension == add_dot_to_not_empty_extension(empty_extension))
