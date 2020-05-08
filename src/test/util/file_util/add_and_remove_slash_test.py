# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Callable, Tuple

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.file_util import add_slash, remove_slash

path_with_slash = 'home/data/src/'
path_without_slash = 'home/data/src'
empty_path_without_slash = ''
empty_path_with_slash = '/'


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.UTIL), reason=TEST_LEVEL.UTIL.value)
class TestAddAndRemoveSlash:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (path_without_slash, path_with_slash),
                        (path_with_slash, path_with_slash),
                        (empty_path_without_slash, empty_path_with_slash),
                        (empty_path_with_slash, empty_path_with_slash)
                    ],
                    ids=[
                        'add_not_existing_slash',
                        'add_existing_slash',
                        'add_not_existing_slash_to_empty_slash',
                        'add_existing_slash_to_empty_slash'
                    ]
                    )
    def param_add_slash_test(request) -> Tuple[str, str]:
        return request.param
    
    def test_add_slash(self, param_add_slash_test: Callable) -> None:
        (in_data, expected_output) = param_add_slash_test
        result_with_added_slash = add_slash(in_data)
        assert result_with_added_slash == expected_output

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (path_without_slash, path_without_slash),
                        (path_with_slash, path_without_slash),
                        (empty_path_without_slash, empty_path_without_slash),
                        (empty_path_with_slash, empty_path_without_slash),
                    ],
                    ids=[
                        'remove_not_existing_slash',
                        'remove_existing_slash',
                        'remove_not_existing_slash_from_empty_slash',
                        'remove_existing_slash_from_empty_slash'
                    ]
                    )
    def param_remove_slash_test(request) -> Tuple[str, str]:
        return request.param

    def test_remove_slash(self, param_remove_slash_test: Callable) -> None:
        (in_data, expected_output) = param_remove_slash_test
        result_with_removed_slash = remove_slash(in_data)
        assert result_with_removed_slash == expected_output
