# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from enum import Enum
from typing import Dict, Tuple

from src.main.util import consts
from src.main.util.consts import TASK, LANGUAGE
from src.main.util.consts import TEST_DATA_PATH
from src.main.util.file_util import get_content_from_file
from src.main.task_scoring.task_checker import remove_compiled_files, FilesDict
from src.main.task_scoring.tasks_tests_handler import check_tasks, create_in_and_out_dict

log = logging.getLogger(consts.LOGGER_NAME)


class SOLUTION(Enum):
    FULL = "full"
    PARTIAL = "partial"
    WRONG = "wrong"
    ERROR = "error"


def get_actual_rate(task: TASK, language: consts.LANGUAGE, code: str, in_and_out_files_dict: FilesDict) -> float:
    return check_tasks([task], code, in_and_out_files_dict, language, False)[0]


def get_source_code(task: TASK, language: consts.LANGUAGE, solution: str) -> str:
    return get_content_from_file(os.path.join(TEST_DATA_PATH, "task_scoring/tasks_tests_handler", task.value,
                                              language.value, solution + ".txt"))


def run_test_task(task: TASK, expected_pairs: Dict[SOLUTION, Tuple[int, int]], language: LANGUAGE) -> None:
    remove_compiled_files()
    in_and_out_files_dict = create_in_and_out_dict(TASK.tasks())
    for s in SOLUTION:
        code = get_source_code(task, language, s.value)
        expected_pair = expected_pairs[s.value]
        expected_rate = expected_pair[1] / expected_pair[0]
        actual_rate = get_actual_rate(task, language, code, in_and_out_files_dict)
        assert expected_rate == actual_rate, \
            f'Actual rate for task {task}, language {language}, solution {s} is wrong, code:\n{code}. ' \
            f'Expected rate = {expected_rate}. Actual rate = {actual_rate}'
