# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from enum import Enum

from src.main.util import consts
from src.test.test_util import LoggedTest
from src.main.preprocessing.preprocessing import __separate_ati_and_other_files

log = logging.getLogger(consts.LOGGER_NAME)


class TEST_DATA(Enum):
    FILES = 'old_files'
    RESULT = 'result'


VALUE_ERROR = 'value_error'


ATI_FILE_1 = consts.TEST_DATA_PATH + '/preprocessing/preprocessing/ide-events_18963327637.58422_2ec6b363dfea2f6e12ea59dbef61c90ef23c4b02.csv'
ATI_FILE_2 = consts.TEST_DATA_PATH + '/preprocessing/preprocessing/ide-events_18963327648.58422_2ec6b363dfea2f6e12ea59dbef61c90ef23c4b02.csv'

FILE_1 = consts.TEST_DATA_PATH + '/preprocessing/preprocessing/Main_203985_1349205394_43223189605.08081_37c0720d12b4f83bb694fc801a8ab7b20b354bdd.csv'
FILE_2 = consts.TEST_DATA_PATH + '/preprocessing/preprocessing/Main_69437_1494035819_963152475617.9932_2c75cd4f24b92a7c95ffe3253c2b1d821784a5b3.csv'
FILE_3 = consts.TEST_DATA_PATH + '/preprocessing/preprocessing/Name_69437_1494035819_963152475617.9932_2c75cd4f24b92a7c95ffe3253c2b1d821784a5b3.csv'

two_ati_case = {
    TEST_DATA.FILES.value: [ATI_FILE_1, ATI_FILE_2, FILE_1],
    TEST_DATA.RESULT.value: ([ATI_FILE_2, FILE_1], ATI_FILE_1)

}

two_same_files_case = {
    TEST_DATA.FILES.value: [ATI_FILE_1, FILE_1, FILE_2],
    TEST_DATA.RESULT.value: ([FILE_1, FILE_2], None)
}

normal_case = {
    TEST_DATA.FILES.value: [ATI_FILE_1, FILE_1, FILE_3],
    TEST_DATA.RESULT.value: ([FILE_1, FILE_3], ATI_FILE_1)
}

without_ati_case = {
    TEST_DATA.FILES.value: [FILE_1, FILE_3],
    TEST_DATA.RESULT.value: ([FILE_1, FILE_3], None)
}


def separate_files(files: list):
    try:
        ct_files, at_file = __separate_ati_and_other_files(files)
    except ValueError:
        return VALUE_ERROR, None
    return ct_files, at_file


def are_pairs_equal(first_pair: tuple, second_pair: tuple):
    return first_pair[0] == second_pair[0] and first_pair[1] == second_pair[1]


def run_test(case: dict):
    ct_files, at_file = separate_files(case[TEST_DATA.FILES.value])
    return are_pairs_equal(case[TEST_DATA.RESULT.value], (ct_files, at_file))


class TestFilterFiles(LoggedTest):

    def test_two_ati_case(self):
        self.assertTrue(run_test(two_ati_case))

    def test_two_same_files_case(self):
        self.assertTrue(run_test(two_same_files_case))

    def test_normal_case(self):
        self.assertTrue(run_test(normal_case))

    def test_without_ati_case(self):
        self.assertTrue(run_test(without_ati_case))
