# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import unittest
from enum import Enum

from src.main.util.file_util import get_name_from_path
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT


class PATHS_TEST_DATA(Enum):
    PATHS = 'paths'
    FILE_NAME = 'file_name'


class EXTENSION(Enum):
    WITH = 'with_extension'
    WITHOUT = 'without_extension'


# We need to check several cases:
# 1. The passed path contains several folders with the file name with different places of '/'
# 1.1 with extension
# 1.2 without extension
path_with_trailing_slash = {EXTENSION.WITHOUT.value: 'home/data/src/file/', EXTENSION.WITH.value: 'home/data/src/file.txt/'}
path_with_leading_slash = {EXTENSION.WITHOUT.value: '/home/data/src/file', EXTENSION.WITH.value: '/home/data/src/file.txt'}
path_with_both_slashes = {EXTENSION.WITHOUT.value: '/home/data/src/file/', EXTENSION.WITH.value: '/home/data/src/file.txt/'}
path_without_slash = {EXTENSION.WITHOUT.value: 'home/data/src/file', EXTENSION.WITH.value: 'home/data/src/file.txt'}
# The right filename for paths above:
right_path_file_name = {EXTENSION.WITHOUT.value: 'file', EXTENSION.WITH.value: 'file.txt'}
# Dict for testing this case
get_file_name_from_path_data = {PATHS_TEST_DATA.PATHS.value: [path_with_trailing_slash, path_with_leading_slash, path_with_both_slashes, path_without_slash],
                                PATHS_TEST_DATA.FILE_NAME.value: right_path_file_name}


# 2. The passed path only contains filename with different places of '/'
# 2.1 with extension
# 2.2 without extension
file_name_with_trailing_slash = {EXTENSION.WITHOUT.value: 'file/', EXTENSION.WITH.value: 'file.txt/'}
file_name_with_leading_slash = {EXTENSION.WITHOUT.value: '/file', EXTENSION.WITH.value: '/file.txt'}
file_name_with_both_slashes = {EXTENSION.WITHOUT.value: '/file/', EXTENSION.WITH.value: '/file.txt/'}
file_name_without_slash = {EXTENSION.WITHOUT.value: 'file', EXTENSION.WITH.value: 'file.txt'}
# The right filename for paths above:
real_file_name = {EXTENSION.WITHOUT.value: 'file', EXTENSION.WITH.value: 'file.txt'}
# Dict for tasting this case
get_file_name_from_file_name_data = {PATHS_TEST_DATA.PATHS.value: [file_name_with_trailing_slash, file_name_with_leading_slash, file_name_with_both_slashes, file_name_without_slash],
                                     PATHS_TEST_DATA.FILE_NAME.value: real_file_name}


def test_paths_data(self, paths_data_dict: dict):
    for path in paths_data_dict[PATHS_TEST_DATA.PATHS.value]:
        # Check ValueError raising
        # If passed path has no extensions, but we want to return a filename with an extension:
        with self.assertRaises(ValueError):
            get_name_from_path(path[EXTENSION.WITHOUT.value], True)

        # If passed path has no extensions, and we want to return a filename without extension:
        file_name = get_name_from_path(path[EXTENSION.WITHOUT.value], False)
        self.assertTrue(file_name == paths_data_dict[PATHS_TEST_DATA.FILE_NAME.value][EXTENSION.WITHOUT.value])

        # If passed path has an extension, and we want to return a filename without extension:
        file_name = get_name_from_path(path[EXTENSION.WITH.value], False)
        self.assertTrue(file_name == paths_data_dict[PATHS_TEST_DATA.FILE_NAME.value][EXTENSION.WITHOUT.value])

        # If passed path has an extension, and we want to return a filename with the extension:
        file_name = get_name_from_path(path[EXTENSION.WITH.value], True)
        self.assertTrue(file_name == paths_data_dict[PATHS_TEST_DATA.FILE_NAME.value][EXTENSION.WITH.value])


class TestGettingFileNameFromPath(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_path(self):
        test_paths_data(self, get_file_name_from_path_data)

    def test_file_name(self):
        test_paths_data(self, get_file_name_from_file_name_data)
