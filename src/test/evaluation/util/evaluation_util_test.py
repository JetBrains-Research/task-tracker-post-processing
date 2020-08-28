# Copyright (c) by anonymous author(s)

from typing import Tuple, List, Callable

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.evaluation.util import contains_at_least_n_true


MAX_N = 5


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.UTIL), reason=TEST_LEVEL.UTIL.value)
class TestEvaluationUtil:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        ([True], 1),
                        ([False], 0),
                        ([False, False], 0),
                        ([True, False], 1),
                        ([False, True], 1),
                        ([True, True], 2),
                        ([False, False, False], 0),
                        ([True, False, False], 1),
                        ([False, True, False], 1),
                        ([False, False, True], 1),
                        ([True, True, False], 2),
                        ([False, True, True], 2),
                        ([True, False, True], 2),
                        ([True, True, True], 3),
                    ])
    def param_contains_at_least_n_true(request) -> Tuple[List[bool], int]:
        return request.param

    def test_param_contains_at_least_n_true(self, param_contains_at_least_n_true: Callable, subtests) -> None:
        (bool_list, max_n_for_true) = param_contains_at_least_n_true

        for i in range(1, max_n_for_true + 1):
            # If for max_n_for_true is True then for i in [1, max_n_for_true] is True too
            with subtests.test(msg=f'Exception was raised for list {bool_list} and min_number_of_true = {i}'):
                assert contains_at_least_n_true(*bool_list, min_number_of_true=i)

        for i in range(max_n_for_true + 1, MAX_N):
            # If for max_n_for_true is True then for i in [max_n_for_true + 1, inf) is False
            with subtests.test(msg=f'Exception was raised for list {bool_list} and min_number_of_true = {i}'):
                assert not contains_at_least_n_true(*bool_list, min_number_of_true=i)

