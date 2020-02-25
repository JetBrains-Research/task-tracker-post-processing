import logging
import unittest

from enum import Enum

from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT
from src.main.util.file_util import get_parent_folder_name, get_parent_folder


class PARENT_FOLDER_TEST_DATA(Enum):
    PATHS = 'paths'
    PARENT_FOLDER_WITHOUT_SLASH = 'parent_folder'
    PARENT_FOLDER_WITH_SLASH = 'parent_folder_with_slash'
    PARENT_FOLDER_NAME = 'parent_folder_name'


empty_path = ''
empty_path_with_slash = '/'
empty_path_data = {PARENT_FOLDER_TEST_DATA.PATHS.value: [empty_path, empty_path_with_slash],
                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH.value: '',
                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH.value: '/',
                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME.value: ''}

single_path = 'path'
single_path_with_leading_slash = '/path'
single_path_with_both_slashes = '/path/'
single_path_with_trailing_slash = 'path/'
single_path_data = {PARENT_FOLDER_TEST_DATA.PATHS.value: [single_path, single_path_with_both_slashes, single_path_with_leading_slash, single_path_with_trailing_slash],
                    PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH.value: '',
                    PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH.value: '/',
                    PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME.value: ''}

path = 'path/folder/data'
path_with_trailing_slash = 'path/folder/data/'
path_without_leading_slash_data = {PARENT_FOLDER_TEST_DATA.PATHS.value: [path, path_with_trailing_slash],
                                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH.value: 'path/folder',
                                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH.value: 'path/folder/',
                                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME.value: 'folder'}
path_with_leading_slash = '/path/folder/data'
path_with_both_slashes = '/path/folder/data/'
path_with_leading_slash_data = {PARENT_FOLDER_TEST_DATA.PATHS.value: [path_with_leading_slash, path_with_both_slashes],
                                PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH.value: '/path/folder',
                                PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH.value: '/path/folder/',
                                PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME.value: 'folder'}


def test_parent_folder(self, dict_data: dict):
    for path in dict_data[PARENT_FOLDER_TEST_DATA.PATHS.value]:
        self.assertEqual(dict_data[PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME.value], get_parent_folder_name(path))
        self.assertEqual(dict_data[PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH.value], get_parent_folder(path, False))
        self.assertEqual(dict_data[PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH.value], get_parent_folder(path, True))


class TestParentFolder(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_empty_path(self):
        test_parent_folder(self, empty_path_data)

    def test_single_path(self):
        test_parent_folder(self, single_path_data)

    def test_path_without_leading_slash(self):
        test_parent_folder(self, path_without_leading_slash_data)

    def test_path_with_leading_slash(self):
        test_parent_folder(self, path_with_leading_slash_data)

