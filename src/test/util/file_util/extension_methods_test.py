# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from typing import Callable

import pytest

from src.test.util import does_skip, TEST_LEVEL
from src.main.util.consts import TEST_DATA_PATH, EXTENSION
from src.main.util.file_util import get_extension_from_file, change_extension_to, create_file, remove_file, \
    remove_directory, create_directory

# Assuming there cannot be any slashes at the end of the file, because path 'home/data/file.txt/ is incorrect

file_with_txt_extension = os.path.join(TEST_DATA_PATH, 'util/file_util/extension_tests/file.txt')
file_with_csv_extension = os.path.join(TEST_DATA_PATH, 'util/file_util/extension_tests/file.csv')
file_without_extension = os.path.join(TEST_DATA_PATH, 'util/file_util/extension_tests/file')
folder_with_slash = os.path.join(TEST_DATA_PATH, 'util/file_util/extension_tests/')

extension_with_dot = EXTENSION.TXT
empty_extension = EXTENSION.EMPTY


def clear_folder(folder) -> None:
    remove_directory(folder)
    create_directory(folder)


@pytest.mark.skipif(does_skip(current_module_level=TEST_LEVEL.UTIL), reason=TEST_LEVEL.UTIL.value)
class TestExtensionMethods:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (file_with_txt_extension, EXTENSION.TXT),
                        (file_without_extension, EXTENSION.EMPTY),
                        (folder_with_slash, EXTENSION.EMPTY),
                    ],
                    ids=[
                        'getting_txt_extension',
                        'getting_empty_extension',
                        'getting_exception_from_folder'
                    ]
                    )
    def param_getting_extension_test(request):
        return request.param

    def test_getting_extension(self, param_getting_extension_test: Callable) -> None:
        (in_data, expected_output) = param_getting_extension_test
        assert expected_output == get_extension_from_file(in_data)

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (file_with_csv_extension, EXTENSION.TXT, file_with_txt_extension),
                        (file_with_csv_extension, EXTENSION.EMPTY, file_without_extension),
                        (file_without_extension, EXTENSION.TXT, file_with_txt_extension),
                    ],
                    ids=[
                        'changing_extension',
                        'changing_to_empty_extension',
                        'changing_empty_extension'
                    ]
                    )
    def param_changing_extension_test(request):
        return request.param

    def test_changing_extension(self, param_changing_extension_test: Callable) -> None:
        (in_data, new_extension, expected_name) = param_changing_extension_test
        clear_folder(folder_with_slash)
        create_file('', in_data)
        change_extension_to(in_data, new_extension, True)
        assert os.path.isfile(expected_name)
        remove_file(expected_name)
