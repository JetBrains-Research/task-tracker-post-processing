import logging
from enum import Enum

from src.main.util import consts
from src.main.util.consts import TEST_DATA_PATH
from src.main.handlers import tasks_tests_handler as tth
from src.main.util.file_util import get_content_from_file
from src.main.handlers.tasks_tests_handler import create_source_code_file

log = logging.getLogger(consts.LOGGER_NAME)


def are_equal(pair_1, pair_2):
    return pair_1[0] == pair_2[0] and pair_1[1] == pair_2[1]


class SOLUTION(Enum):
    FULL = "full"
    PARTIAL = "partial"
    WRONG = "wrong"
    ERROR = "error"


def get_actual_pair(task: str, language: str, code: str):
    source_file_name = create_source_code_file(code, language)
    log.info("Source code:\n" + code)
    return tth.check_task(task, source_file_name, language)


def get_source_code(task: str, language: str, solution: str):
    return get_content_from_file(TEST_DATA_PATH + "/tasks_tests_handler/" + task + "/"
                                 + language + "/" + solution + ".txt")


def test_task(self, actual_pairs, language):
    tth.__remove_compiled_files()
    for s in SOLUTION:
        code = get_source_code(self.task, language, s.value)
        actual_pair = actual_pairs[s.value]
        expected_pair = get_actual_pair(self.task, language, code)
        self.assertTrue(are_equal(actual_pair, expected_pair))
