# Copyright (c) by anonymous author(s)

from typing import Tuple

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.strings_util import convert_camel_case_to_snake_case

data = [('considerMeAsOneWhoLovedPoetryAndPersimmons', 'consider_me_as_one_who_loved_poetry_and_persimmons'),
        ('ResponseHTTP23', 'response_http_23'),
        ('maxDigit', 'max_digit'),
        ('max3', 'max_3'),
        ('already_snake_case', 'already_snake_case'),
        ('pies', 'pies'),
        ('WRITE_TASK', 'write_task'),
        ('', ''),
        ('13.0', '13.0'),
        ('IAm11.0YearsOld', 'i_am_11.0_years_old'),
        ('aB', 'a_b')]


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.UTIL), reason=TEST_LEVEL.UTIL.value)
class TestConversionToSnakeCase:

    @pytest.mark.parametrize('d', [_ for _ in data])
    def test_upper_letters(self, d: Tuple[str, str]) -> None:
        camel_case, snake_case = d
        converted_snake_case = convert_camel_case_to_snake_case(camel_case)
        assert snake_case == converted_snake_case, f'{converted_snake_case} is not equal {snake_case}'

