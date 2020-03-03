import logging
import unittest

from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT
from src.main.util.strings_util import convert_camel_case_to_snake_case

data = [['considerMeAsOneWhoLovedPoetryAndPersimmons', 'consider_me_as_one_who_loved_poetry_and_persimmons'],
        ['ResponseHTTP23', 'response_http_23'],
        ['maxDigit', 'max_digit'],
        ['max3', 'max_3'],
        ['already_snake_case', 'already_snake_case'],
        ['pies', 'pies'],
        ['WRITE_TASK', 'write_task'],
        ['', '']]


class TestConversionToSnakeCase(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def testUpperLetters(self):
        for d in data:
            camel_case = d[0]
            snake_case = d[1]
            converted_snake_case = convert_camel_case_to_snake_case(camel_case)
            self.assertEqual(converted_snake_case, snake_case, msg=f'{converted_snake_case} is not equal {snake_case}')