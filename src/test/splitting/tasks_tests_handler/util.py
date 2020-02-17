import logging
from enum import Enum

from src.main.util import consts
from src.main.util.consts import TASK
from src.main.util.consts import TEST_DATA_PATH
from src.main.splitting import tasks_tests_handler as tth
from src.main.util.file_util import get_content_from_file

log = logging.getLogger(consts.LOGGER_NAME)


class SOLUTION(Enum):
    FULL = "full"
    PARTIAL = "partial"
    WRONG = "wrong"
    ERROR = "error"


def get_actual_rate(task: str, language: str, code: str, in_and_out_files_dict: dict):
    return tth.check_tasks([task], code, in_and_out_files_dict, language, False)[0]


def get_source_code(task: str, language: str, solution: str):
    return get_content_from_file(TEST_DATA_PATH + "/splitting/tasks_tests_handler/" + task + "/"
                                 + language + "/" + solution + ".txt")


def get_tasks():
    tasks = []
    for t in TASK:
        tasks.append(t.value)
    return tasks


def test_task(self, expected_pairs, language):
    tth.__remove_compiled_files()
    in_and_out_files_dict = tth.create_in_and_out_dict(get_tasks())
    for s in SOLUTION:
        code = get_source_code(self.task, language, s.value)
        expected_pair = expected_pairs[s.value]
        expected_rate = expected_pair[1] / expected_pair[0]
        actual_rate = get_actual_rate(self.task, language, code, in_and_out_files_dict)
        self.assertEqual(expected_rate, actual_rate)

