# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
import ast
import enum
import logging
import pandas as pd

from src.main.util import consts
from typing import Tuple, List, Union, Any
from src.main.util.consts import EXPERIENCE, DEFAULT_VALUES
from src.main.splitting.splitting import unpack_tests_results
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.file_util import get_all_file_system_items, csv_file_condition
from src.main.canonicalization.canonicalization import get_canonicalized_form, are_asts_equal
from src.main.solution_space.data_classes import AtiItem, Profile, User, Code, CodeInfo

log = logging.getLogger(consts.LOGGER_NAME)

COLUMN_TYPE = Union[consts.CODE_TRACKER_COLUMN, consts.ACTIVITY_TRACKER_COLUMN]


def __get_column_value(solutions: pd.DataFrame, index: int, column: COLUMN_TYPE) -> Any:
    return solutions[column.value].iloc[index]


def __get_column_unique_value(solutions: pd.DataFrame, column: COLUMN_TYPE, default: Any) -> Any:
    column = column.value
    unique_values = solutions[column].unique()
    if len(unique_values) == 0:
        log.info(f'Unique values not found')
        return default
    if len(unique_values) > 1:
        log.error(f'There is more than 1 unique value in column {column}: {unique_values}')
        raise ValueError(f'There is more than 1 unique value in column {column}: {unique_values}')
    return unique_values[0]


def __get_enum_or_default(enum_meta: enum.EnumMeta, value: str, default: DEFAULT_VALUES) \
        -> Union[enum.EnumMeta, DEFAULT_VALUES]:
    return enum_meta._value2member_map_.get(value, default)


def __get_ati_data(solutions: pd.DataFrame, index: int) -> AtiItem:
    timestamp = __get_column_value(solutions, index, consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI)
    str_event_type = __get_column_value(solutions, index, consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE)
    event_type = __get_enum_or_default(consts.ACTIVITY_TRACKER_EVENTS, str_event_type, DEFAULT_VALUES.EVENT_TYPE)
    event_data = __get_column_value(solutions, index, consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA)
    return AtiItem(timestamp=timestamp, event_type=event_type, event_data=event_data)


def __are_same_fragments(current_tree: ast.AST, solutions: pd.DataFrame, next_index: int) -> bool:
    fragment = __get_column_value(solutions, next_index, consts.CODE_TRACKER_COLUMN.FRAGMENT)
    next_tree = get_canonicalized_form(fragment)
    return are_asts_equal(current_tree, next_tree)


# Get ati data and add it to the ati_elements list if it is not empty
def __handle_current_ati(ati_elements: list, solutions: pd.DataFrame, index: int) -> None:
    ati_element = __get_ati_data(solutions, index)
    if not ati_element.is_empty():
        log.info(f'Find not empty ati element: {ati_element}')
        ati_elements.append(ati_element)


# Find the same code fragments in data and construct list of ati items for this fragment
def __find_same_fragments(solutions: pd.DataFrame, start_index: int) -> Tuple[int, List[AtiItem], ast.AST]:
    i, ati_elements = start_index + 1, []
    __handle_current_ati(ati_elements, solutions, start_index)
    current_fragment = __get_column_value(solutions, start_index, consts.CODE_TRACKER_COLUMN.FRAGMENT)
    current_tree = get_canonicalized_form(current_fragment)

    while i < solutions.shape[0] and __are_same_fragments(current_tree, solutions, i):
        __handle_current_ati(ati_elements, solutions, i)
        i += 1
    return i, ati_elements, current_tree


def __get_profile(solutions: pd.DataFrame) -> Profile:
    # Data should be preprocessed so in 'age' and 'experience' columns should be only 1 unique value for each column
    age = __get_column_unique_value(solutions, consts.CODE_TRACKER_COLUMN.AGE, consts.DEFAULT_VALUES.AGE.value)
    str_experience = __get_column_unique_value(solutions, consts.CODE_TRACKER_COLUMN.EXPERIENCE,
                                               consts.DEFAULT_VALUES.EXPERIENCE.value)
    experience = __get_enum_or_default(EXPERIENCE, str_experience, DEFAULT_VALUES.EXPERIENCE)
    return Profile(age=age, experience=experience)


def __get_user(solutions: pd.DataFrame) -> User:
    return User(__get_profile(solutions))


def __get_code_info(solutions: pd.DataFrame, user: User, index: int, ati_actions: List[AtiItem]) -> CodeInfo:
    date = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.DATE)
    timestamp = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.TIMESTAMP)
    return CodeInfo(user, timestamp, date, ati_actions)


def __is_compiled(test_result: int) -> bool:
    return test_result != consts.TEST_RESULT.INCORRECT_CODE.value


def __is_correct_fragment(tests_results: str) -> bool:
    tasks = consts.TASK.tasks_values()
    tests_results = unpack_tests_results(tests_results, tasks)
    compiled_task_count = len([t for i, t in enumerate(tasks) if __is_compiled(tests_results[i])])
    # It is an error, if a part of the tasks is incorrect, but another part is correct.
    # For example: [-1,1,0.5,0.5,-1,-1]
    if 0 < compiled_task_count < len(tasks):
        log.error(f'A part of the tasks is incorrect, but another part is correct: {tests_results}')
        raise ValueError(f'A part of the tasks is incorrect, but another part is correct: {tests_results}')
    return compiled_task_count == len(tasks)


def __filter_incorrect_fragments(solutions: pd.DataFrame) -> pd.DataFrame:
    return solutions.loc[solutions[consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value].apply(__is_correct_fragment)]


def __get_task_index(task: str) -> int:
    return consts.TASK.tasks_values().index(task)


def __get_rate(tests_results: str, task_index: int) -> float:
    tasks = consts.TASK.tasks_values()
    tests_results = unpack_tests_results(tests_results, tasks)
    if task_index >= len(tasks) or task_index >= len(tests_results):
        log.error(f'Task index {task_index} is more than length of tasks list')
        raise ValueError(f'Task index {task_index} is more than length of tasks list')
    return tests_results[task_index]


def __get_code(solutions: pd.DataFrame, index: int, task_index: int, tree: ast.AST) -> Code:
    tests_results = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.TESTS_RESULTS)
    rate = __get_rate(tests_results, task_index)
    log.info(f'Task index is :{task_index}, rate is: {rate}')
    return Code(ast=tree, rate=rate)


def __convert_to_datetime(df: pd.DataFrame) -> None:
    for column in [consts.CODE_TRACKER_COLUMN.DATE, consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI]:
        df[column.value] = pd.to_datetime(df[column.value], errors='ignore')


def __add_user_solutions(file: str, task: str) -> List[Tuple[Code, CodeInfo]]:
    log.info(f'Start solution space creating for file {file} for task {task}')
    data = pd.read_csv(file, encoding=consts.ISO_ENCODING)
    __convert_to_datetime(data)
    solutions = __filter_incorrect_fragments(data)
    log.info(f'Size of solutions after filtering incorrect fragments is {solutions.shape[0]}')
    task_index = __get_task_index(task)
    i, code_info_chain = 0, []
    user = __get_user(solutions)
    while i < solutions.shape[0]:
        old_index = i
        i, ati_actions, tree = __find_same_fragments(solutions, i)
        code = __get_code(solutions, old_index, task_index, tree)
        code_info = __get_code_info(solutions, user, old_index, ati_actions)
        code_info_chain.append((code, code_info))
    log.info(f'Finish solution space creating for file {file} for task {task}')
    return code_info_chain


def construct_solution_graph(path: str, task: str,) -> SolutionGraph:
    files = get_all_file_system_items(path, csv_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    sg = SolutionGraph()
    log.info(f'Start creating of solution space')
    for file in files:
        log.info(f'Start handling file {file}')
        code_info_chain = __add_user_solutions(file, task)
        sg.add_code_info_chain(code_info_chain)
    log.info(f'Finish creating of solution space')
    return sg
