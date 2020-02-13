import logging
import unittest
from enum import Enum

from src.main.util import consts
from src.main.preprocessing.preprocessing import __separate_at_and_other_files

log = logging.getLogger(consts.LOGGER_NAME)


class DATA(Enum):
    FILES = 'old_files'
    RESULT = 'result'
    ERROR = 'error'


ATI_FILE_1 = '/path/ide-events_18963327637.58422_2ec6b363dfea2f6e12ea59dbef61c90ef23c4b02.csv'
ATI_FILE_2 = '/path/ide-events_18963327648.58422_2ec6b363dfea2f6e12ea59dbef61c90ef23c4b02.csv'

FILE_1 = '/path/Main_203985_1349205394_43223189605.08081_37c0720d12b4f83bb694fc801a8ab7b20b354bdd.csv'
FILE_2 = '/path/Main_69437_1494035819_963152475617.9932_2c75cd4f24b92a7c95ffe3253c2b1d821784a5b3.csv'
FILE_3 = '/path/Name_69437_1494035819_963152475617.9932_2c75cd4f24b92a7c95ffe3253c2b1d821784a5b3.csv'

two_ati_case = {
    DATA.FILES.value: [ATI_FILE_1, ATI_FILE_2, FILE_1],
    DATA.RESULT.value: (DATA.ERROR.value, None)
}

two_same_files_case = {
    DATA.FILES.value: [ATI_FILE_1, FILE_1, FILE_2],
    DATA.RESULT.value: ([FILE_1, FILE_2], None)
}

normal_case = {
    DATA.FILES.value: [ATI_FILE_1, FILE_1, FILE_3],
    DATA.RESULT.value: ([FILE_1, FILE_2], ATI_FILE_1)
}

without_ati_case = {
    DATA.FILES.value: [FILE_1, FILE_3],
    DATA.RESULT.value: ([FILE_1, FILE_2], None)
}


def separate_files(files: list):
    try:
        ct_files, at_file = __separate_at_and_other_files(files)
    except ValueError:
        return DATA.ERROR.value, None
    return ct_files, at_file


def equal_result(actual_pair: tuple, real_pair: tuple):
    return actual_pair[0] == real_pair[0] and actual_pair[1] == real_pair[1]


def run_test(case: dict):
    ct_files, at_file = separate_files(case[DATA.FILES.value])
    return equal_result(case[ DATA.RESULT.value], (ct_files, at_file))


class TestFilterFiles(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=consts.LOGGER_TEST_FILE, level=logging.INFO)

    def test_two_ati_case(self):
        self.assertTrue(two_ati_case)

    def test_two_same_files_case(self):
        self.assertTrue(two_same_files_case)

    def test_normal_case(self):
        self.assertTrue(normal_case)

    def test_without_ati_case(self):
        self.assertTrue(without_ati_case)
