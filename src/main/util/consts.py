# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from enum import Enum

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

LOGGER_NAME = 'main_logger'
LOGGER_FILE = ROOT_DIR + '../../../../logs.log'
LOGGER_TEST_FILE = ROOT_DIR + '../../../../test_logs.log'
LOGGER_FORMAT = '%(asctime)s:%(levelname)s ==> %(message)s'

TEST_PATH = ROOT_DIR + '/../../test'

class FILE_SYSTEM_ITEM(Enum):
    PATH = 0
    SUBDIR = 1
    FILE = 2

class CANONIZATION_TESTS(Enum):
    TASKS_TESTS_PATH = ROOT_DIR + '/../../resources'
    INPUT_FILE_NAME = 'in'
    OUTPUT_FILE_NAME = 'out'

class CANONIZATION_TESTS_TYPES(Enum):
    CLEANED_CODE = 'cleaned_code'
    ANONYMIZE_NAMES = 'anonymize_names'
    CANONICAL_FORM = 'canonical_form'
