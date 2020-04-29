# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from enum import Enum
from typing import Dict, Union, List, Callable

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.file_util import get_parent_folder_name, get_parent_folder


class PARENT_FOLDER_TEST_DATA(Enum):
    PATHS = 'paths'
    PARENT_FOLDER_WITHOUT_SLASH = 'parent_folder'
    PARENT_FOLDER_WITH_SLASH = 'parent_folder_with_slash'
    PARENT_FOLDER_NAME = 'parent_folder_name'


DictData = Dict[PARENT_FOLDER_TEST_DATA, Union[List[str], str]]

empty_path = ''
empty_path_with_slash = '/'
empty_path_data = {PARENT_FOLDER_TEST_DATA.PATHS: [empty_path, empty_path_with_slash],
                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH: '',
                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH: '/',
                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME: ''}

single_path = 'path'
single_path_with_leading_slash = '/path'
single_path_with_both_slashes = '/path/'
single_path_with_trailing_slash = 'path/'
single_path_data = {PARENT_FOLDER_TEST_DATA.PATHS: [single_path, single_path_with_both_slashes, single_path_with_leading_slash, single_path_with_trailing_slash],
                    PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH: '',
                    PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH: '/',
                    PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME: ''}

path = 'path/folder/data'
path_with_trailing_slash = 'path/folder/data/'
path_without_leading_slash_data = {PARENT_FOLDER_TEST_DATA.PATHS: [path, path_with_trailing_slash],
                                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH: 'path/folder',
                                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH: 'path/folder/',
                                   PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME: 'folder'}
path_with_leading_slash = '/path/folder/data'
path_with_both_slashes = '/path/folder/data/'
path_with_leading_slash_data = {PARENT_FOLDER_TEST_DATA.PATHS: [path_with_leading_slash, path_with_both_slashes],
                                PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH: '/path/folder',
                                PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH: '/path/folder/',
                                PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME: 'folder'}


def run_test(dict_data: DictData) -> None:
    for path in dict_data[PARENT_FOLDER_TEST_DATA.PATHS]:
        assert dict_data[PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_NAME] == get_parent_folder_name(path)
        assert dict_data[PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITHOUT_SLASH] == get_parent_folder(path, False)
        assert dict_data[PARENT_FOLDER_TEST_DATA.PARENT_FOLDER_WITH_SLASH] == get_parent_folder(path, True)


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.UTIL), reason=TEST_LEVEL.UTIL.value)
class TestParentFolder:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        empty_path_data,
                        single_path_data,
                        path_without_leading_slash_data,
                        path_with_leading_slash_data
                    ])
    def param_parent_folder_test(request) -> DictData:
        return request.param

    def test_parent_folder(self, param_parent_folder_test: Callable) -> None:
        data_dict = param_parent_folder_test
        run_test(data_dict)
