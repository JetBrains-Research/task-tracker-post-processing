# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from enum import Enum
from typing import Dict, Union, List

import pytest

from src.test.util import to_skip, TEST_LEVEL
from src.main.util.file_util import get_name_from_path


class PATHS_TEST_DATA(Enum):
    PATHS = 'paths'
    FILE_NAME = 'file_name'


class EXTENSION(Enum):
    WITH = 'with_extension'
    WITHOUT = 'without_extension'


PathsDataDict = Dict[PATHS_TEST_DATA, Union[List[Dict[EXTENSION, str]], Dict[EXTENSION, str]]]

# We need to check several cases:
# 1. The passed path contains several folders with the file name with different places of '/'
# 1.1 with extension
# 1.2 without extension
path_with_trailing_slash = {EXTENSION.WITHOUT: 'home/data/src/file/', EXTENSION.WITH: 'home/data/src/file.txt/'}
path_with_leading_slash = {EXTENSION.WITHOUT: '/home/data/src/file', EXTENSION.WITH: '/home/data/src/file.txt'}
path_with_both_slashes = {EXTENSION.WITHOUT: '/home/data/src/file/', EXTENSION.WITH: '/home/data/src/file.txt/'}
path_without_slash = {EXTENSION.WITHOUT: 'home/data/src/file', EXTENSION.WITH: 'home/data/src/file.txt'}
# The right filename for paths above:
right_path_file_name = {EXTENSION.WITHOUT: 'file', EXTENSION.WITH: 'file.txt'}
# Dict for testing this case
file_name_from_path_data_dict = {PATHS_TEST_DATA.PATHS: [path_with_trailing_slash, path_with_leading_slash,
                                                         path_with_both_slashes, path_without_slash],
                                 PATHS_TEST_DATA.FILE_NAME: right_path_file_name}


# 2. The passed path only contains filename with different places of '/'
# 2.1 with extension
# 2.2 without extension
file_name_with_trailing_slash = {EXTENSION.WITHOUT: 'file/', EXTENSION.WITH: 'file.txt/'}
file_name_with_leading_slash = {EXTENSION.WITHOUT: '/file', EXTENSION.WITH: '/file.txt'}
file_name_with_both_slashes = {EXTENSION.WITHOUT: '/file/', EXTENSION.WITH: '/file.txt/'}
file_name_without_slash = {EXTENSION.WITHOUT: 'file', EXTENSION.WITH: 'file.txt'}
# The right filename for paths above:
real_file_name = {EXTENSION.WITHOUT: 'file', EXTENSION.WITH: 'file.txt'}
# Dict for tasting this case
file_name_from_file_name_data_dict = {PATHS_TEST_DATA.PATHS: [file_name_with_trailing_slash,
                                                              file_name_with_leading_slash,
                                                              file_name_with_both_slashes,
                                                              file_name_without_slash],
                                      PATHS_TEST_DATA.FILE_NAME: real_file_name}


def run_test(paths_data_dict: PathsDataDict) -> None:
    for path in paths_data_dict[PATHS_TEST_DATA.PATHS]:
        # Check ValueError raising if passed path has no extensions, but we want to return a filename with an extension:
        with pytest.raises(ValueError):
            get_name_from_path(path[EXTENSION.WITHOUT], True)

        # If passed path has no extensions, and we want to return a filename without extension:
        file_name = get_name_from_path(path[EXTENSION.WITHOUT], False)
        assert file_name == paths_data_dict[PATHS_TEST_DATA.FILE_NAME][EXTENSION.WITHOUT]

        # If passed path has an extension, and we want to return a filename without extension:
        file_name = get_name_from_path(path[EXTENSION.WITH], False)
        assert file_name == paths_data_dict[PATHS_TEST_DATA.FILE_NAME][EXTENSION.WITHOUT]

        # If passed path has an extension, and we want to return a filename with the extension:
        file_name = get_name_from_path(path[EXTENSION.WITH], True)
        assert file_name == paths_data_dict[PATHS_TEST_DATA.FILE_NAME][EXTENSION.WITH]


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.UTIL), reason=TEST_LEVEL.UTIL.value)
class TestGettingFileNameFromPath:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        file_name_from_path_data_dict,
                        file_name_from_file_name_data_dict
                    ],
                    ids=[
                        'test_path',
                        'test_file_name'
                    ]
                    )
    def param_get_file_name_test(request) -> PathsDataDict:
        return request.param

    def test_paths_data(self, param_get_file_name_test):
        run_test(param_get_file_name_test)
