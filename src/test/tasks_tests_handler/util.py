from enum import Enum

from src.main.handlers import tasks_tests_handler as tth


def are_equal(pair_1, pair_2):
    return pair_1[0] == pair_2[0] and pair_1[1] == pair_2[1]


class SOLUTION(Enum):
    FULL = "FULL",
    PARTIAL = "PARTIAL",
    WRONG = "WRONG",
    ERROR = "ERROR"


def get_actual_pair(task, language: str, code: str):
    return tth.check_task(task, code, language)


def test_task(self, test_data, language):
    tth.__remove_compiled_files()
    for s in SOLUTION:
        code = test_data[s.value][0]
        actual_pair = test_data[s.value][1]
        expected_pair = get_actual_pair(self.task, language, code)
        self.assertTrue(are_equal(actual_pair, expected_pair))