# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Tuple

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.time_util import corrected_time


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.UTIL), reason=TEST_LEVEL.UTIL.value)
class TestTimeMethods:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        ('2019-12-09T18:41:28.548+03:00', '2019-12-09T18:41:28.548+0300'),
                        ('2019-12-09T18:41:28.548-03:00', '2019-12-09T18:41:28.548-0300')
                    ],
                    ids=['positive_time', 'negative_time']
                    )
    def param_test(request) -> Tuple[str, str]:
        return request.param

    def test_corrected_time(self, param_test) -> None:
        (in_data, expected_output) = param_test
        result = corrected_time(in_data)
        assert result == expected_output
