import logging
from enum import Enum

from src.main.util import consts
from src.main.util.consts import TASK
from src.main.util.consts import TEST_DATA_PATH
from src.main.handlers import tasks_tests_handler as tth
from src.main.util.file_util import get_content_from_file
from src.main.handlers.tasks_tests_handler import __create_source_code_file

log = logging.getLogger(consts.LOGGER_NAME)


class SOLUTION(Enum):
    FULL = "full"
    PARTIAL = "partial"
    WRONG = "wrong"
    ERROR = "error"


def get_expected_rate(task: str, language: str, code: str, in_and_out_files_dict: dict):
    return tth.check_tasks([task], code, in_and_out_files_dict, language)[0]


def get_source_code(task: str, language: str, solution: str):
    return get_content_from_file(TEST_DATA_PATH + "/tasks_tests_handler/" + task + "/"
                                 + language + "/" + solution + ".txt")


def get_tasks():
    tasks = []
    for t in TASK:
        tasks.append(t.value)
    return tasks


def test_task(self, actual_pairs, language):
    tth.__remove_compiled_files()
    in_and_out_files_dict = tth.create_in_and_out_dict(get_tasks())
    for s in SOLUTION:
        code = get_source_code(self.task, language, s.value)
        actual_pair = actual_pairs[s.value]
        actual_rate = actual_pair[1] / actual_pair[0]
        expected_rate = get_expected_rate(self.task, language, code, in_and_out_files_dict)
        self.assertEqual(actual_rate, expected_rate)
