import logging
import unittest

from src.main.util import consts
from src.main.util.consts import TASK, LOGGER_TEST_FILE
from src.splitting.consts import SPLIT_DICT
from src.splitting.splitting import find_real_splits

INDEX = SPLIT_DICT.INDEX.value
RATE = SPLIT_DICT.RATE.value
TASKS = SPLIT_DICT.TASKS.value

PIES = TASK.PIES.value
ZERO = TASK.ZERO.value
MAX_3 = TASK.MAX_3.value
MAX_DIGIT = TASK.MAX_DIGIT.value
BRACKETS = TASK.BRACKETS.value
ELECTION = TASK.ELECTION.value

supposed_splits_large = [
    {INDEX: 10,
     RATE: 0.1,
     TASKS: [PIES, MAX_3, ELECTION]},
    {INDEX: 30,
     RATE: 0.2,
     TASKS: [PIES, MAX_3]},
    {INDEX: 40,
     RATE: 0.5,
     TASKS: [PIES, MAX_3]},
    {INDEX: 45,
     RATE: 0.5,
     TASKS: [PIES]},
    {INDEX: 90,
     RATE: 1.0,
     TASKS: [PIES]},
    {INDEX: 100,
     RATE: 0.5,
     TASKS: [MAX_3, ZERO]},
    {INDEX: 110,
     RATE: 0.5,
     TASKS: [PIES, MAX_3]},
    {INDEX: 115,
     RATE: 0.9,
     TASKS: [ELECTION]},
    {INDEX: 130,
     RATE: 0.5,
     TASKS: [ELECTION]},
]

expected_real_splits_large = [
    {INDEX: 90,
     RATE: 1.0,
     TASKS: [PIES]},
    {INDEX: 110,
     RATE: 0.5,
     TASKS: [MAX_3]},
    {INDEX: 130,
     RATE: 0.5,
     TASKS: [ELECTION]}
]

supposed_splits_small = [
    {INDEX: 90,
     RATE: 1.0,
     TASKS: [PIES]}
]

expected_real_splits_small = [
    {INDEX: 90,
     RATE: 1.0,
     TASKS: [PIES]}
]

supposed_splits_medium = [
    {INDEX: 90,
     RATE: 1.0,
     TASKS: [PIES]},
    {INDEX: 900,
     RATE: 0.3,
     TASKS: [ELECTION, BRACKETS]}
]

expected_real_splits_medium = [
    {INDEX: 90,
     RATE: 1.0,
     TASKS: [PIES]},
    {INDEX: 900,
     RATE: 0.3,
     TASKS: [ELECTION, BRACKETS]}
]

supposed_splits_empty = []
expected_real_splits_empty = []


class TestPiesTests(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, level=logging.INFO)

    def test_find_real_splits_large(self):
        actual_real_splits = find_real_splits(supposed_splits_large)
        self.assertTrue(actual_real_splits == expected_real_splits_large)

    def test_find_real_splits_medium(self):
        actual_real_splits = find_real_splits(supposed_splits_medium)
        self.assertTrue(actual_real_splits == expected_real_splits_medium)

    def test_find_real_splits_small(self):
        actual_real_splits = find_real_splits(supposed_splits_small)
        self.assertTrue(actual_real_splits == expected_real_splits_small)

    def test_find_real_splits_empty(self):
        actual_real_splits = find_real_splits(supposed_splits_empty)
        self.assertTrue(actual_real_splits == expected_real_splits_empty)
