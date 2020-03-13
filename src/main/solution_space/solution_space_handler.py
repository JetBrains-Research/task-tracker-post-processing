# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina


import logging
import pandas as pd

from src.main.util import consts
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.data_classes import AtiItem, Profile, User
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


# Find the same code fragments in data and construnct list of ati items for this fragment
def __find_same_fragments(solutions: pd.DataFrame, start_index: int) -> tuple:
    i, ati_elements = start_index, []
    current_fragment = __get_column_value(solutions, start_index, consts.CODE_TRACKER_COLUMN.FRAGMENT.value)
    while i < solutions.shape[0] - 1:
        next_fragment = __get_column_value(solutions, i + 1, consts.CODE_TRACKER_COLUMN.FRAGMENT.value)
        if current_fragment != next_fragment:
            return i, ati_elements
        ati_elements.append(__get_ati_data(solutions, i))
        i += 1
    return i, ati_elements


def __get_profile(solutions: pd.DataFrame, index: int) -> Profile:
    age = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.AGE.value)
    experience = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.EXPERIENCE.value)
    return Profile(age=age, experience=experience)


def __get_user(solutions: pd.DataFrame, index: int, profile: Profile) -> User:
    date = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.DATE.value)
    timestamp = __get_column_value(solutions, index, consts.CODE_TRACKER_COLUMN.TIMESTAMP.value)
    return User(date=date, timestamp=timestamp, profile=profile)


def __add_user_solutions(file: str, sg: SolutionGraph) -> SolutionGraph:
    log.info(f'Start solution space creating file {file}')
    solutions = pd.read_csv(file, encoding=consts.ISO_ENCODING)
    i = 0
    while i < solutions.shape[0]:
        profile = __get_profile(solutions, i)
        user = __get_user(solutions, i, profile)
        fragment = __get_column_value(solutions, i, consts.CODE_TRACKER_COLUMN.FRAGMENT.value)
        canon_tree = get_canonicalized_form(fragment)
        i, ati_elements = __find_same_fragments(solutions, i)
        # Todo: add Vertex to graph: profile, user, canon_tree, ati_elements
        pass
    return sg


def construct_solution_graph(path: str) -> SolutionGraph:
    files = get_all_file_system_items(path, csv_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    sg = SolutionGraph()
    for file in files:
        sg = __add_user_solutions(file, sg)
    return sg
