# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import pandas as pd

from typing import Tuple, List
from src.main.util import consts
from src.main.splitting.splitting import unpack_tests_results
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.data_classes import AtiItem, Profile, User, Code
from src.main.canonicalization.canonicalization import get_canonicalized_form
from src.main.util.file_util import get_all_file_system_items, csv_file_condition


log = logging.getLogger(consts.LOGGER_NAME)


def __get_column_value(solutions: pd.DataFrame, index: int, column=None) -> str:
    return solutions[column].iloc[index]


def __get_ati_data(solutions: pd.DataFrame, index: int) -> AtiItem:
    timestamp = __get_column_value(solutions, index, consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value)
    event_type = __get_column_value(solutions, index, consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value)
    event_data = __get_column_value(solutions, index, consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value)
    return AtiItem(timestamp=timestamp, event_type=event_type, event_data=event_data)


def __is_last_index(collection_size: int, index: int) -> bool:
    return index == collection_size - 1


def __are_same_fragments(fragment_1: str, fragment_2: str) -> bool:
    return fragment_1 == fragment_2


def __get_empty_fragment() -> str:
    return ''


# Find the same code fragments in data and construct list of ati items for this fragment
def __find_same_fragments(solutions: pd.DataFrame, start_index: int) -> Tuple[int, List[AtiItem]]:
    i, ati_elements = start_index, []
    current_fragment, next_fragment = __get_empty_fragment(), __get_empty_fragment()

    while __are_same_fragments(current_fragment, next_fragment) and not __is_last_index(solutions.shape[0] - 1, i):
        current_fragment = __get_column_value(solutions, start_index, consts.CODE_TRACKER_COLUMN.FRAGMENT.value)
        next_fragment = __get_column_value(solutions, i + 1, consts.CODE_TRACKER_COLUMN.FRAGMENT.value)
        ati_element = __get_ati_data(solutions, i)
        if not ati_element.is_empty():
            log.info(f'Find not empty ati element: {ati_element}')
            ati_elements.append(ati_element)
        i += 1
    return i, ati_elements


def __get_profile(solutions: pd.DataFrame, index: int) -> Profile:
    age = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.AGE.value)
    experience = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.EXPERIENCE.value)
    return Profile(age=age, experience=experience)


def __get_user(solutions: pd.DataFrame, index: int, ati_actions: List[AtiItem]) -> User:
    profile = __get_profile(solutions, index)
    date = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.DATE.value)
    timestamp = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.TIMESTAMP.value)
    return User(date=date, timestamp=timestamp, profile=profile, ati_actions=ati_actions)


def __is_compiled(test_result: int) -> bool:
    return test_result != consts.TEST_RESULT.INCORRECT_CODE.value


def __is_correct_fragment(tests_results: str) -> bool:
    tasks = consts.TASK.tasks()
    tests_results = unpack_tests_results(tests_results, tasks)
    compiled_task = [t for i, t in enumerate(tasks) if __is_compiled(tests_results[i])]
    return len(compiled_task) > 0


def __filter_incorrect_fragments(solutions: pd.DataFrame) -> pd.DataFrame:
    return solutions.loc[solutions[consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value].apply(__is_correct_fragment)]


def __get_task_index(task: str) -> int:
    return consts.TASK.tasks().index(task)


def __get_rate(tests_results: str, task_index: int) -> float:
    tasks = consts.TASK.tasks()
    tests_results = unpack_tests_results(tests_results, tasks)
    if task_index >= len(tasks) or task_index >= len(tests_results):
        log.error(f'Task index {task_index} is more than length of tasks list')
        raise ValueError(f'Task index {task_index} is more than length of tasks list')
    return tests_results[task_index]


def __get_code(solutions: pd.DataFrame, index: int, task_index: int) -> Code:
    fragment = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.FRAGMENT.value)
    log.info(f'Start getting canonicalized form for code:\n{fragment}')
    canon_tree = get_canonicalized_form(fragment)
    log.info(f'Finish getting canonicalized form for code:\n{fragment}')

    tests_results = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value)
    rate = __get_rate(tests_results, task_index)
    log.info(f'Task index is :{task_index}, rate is: {rate}')
    return Code(ast=canon_tree, rate=rate)


def __add_user_solutions(file: str, task: str) -> List[Tuple[Code, User]]:
    log.info(f'Start solution space creating file {file} for task {task}')
    solutions = __filter_incorrect_fragments(pd.read_csv(file, encoding=consts.ISO_ENCODING))
    log.info(f'Size of solutions after filtering incorrect fragments is {solutions.shape[0]}')
    task_index = __get_task_index(task)
    i, code_user_chain = 0, []
    while i < solutions.shape[0]:
        old_index = i
        i, ati_actions = __find_same_fragments(solutions, i)
        code = __get_code(solutions, old_index, task_index)
        user = __get_user(solutions, old_index, ati_actions)
        code_user_chain.append((code, user))
    log.info(f'Finish solution space creating file {file} for task {task}')
    return code_user_chain


def construct_solution_graph(path: str, task: str,) -> SolutionGraph:
    files = get_all_file_system_items(path, csv_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    sg = SolutionGraph()
    log.info(f'Start creating of solution space')
    for file in files:
        log.info(f'Start handling file {file}')
        code_user_chain = __add_user_solutions(file, task)
        # Todo: add items from user_code_chain to sg
        pass
    log.info(f'Finish creating of solution space')
    return sg
