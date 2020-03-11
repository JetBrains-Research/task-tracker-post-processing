import logging
import pandas as pd

from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.file_util import get_all_file_system_items, csv_file_condition

from src.main.util import consts

log = logging.getLogger(consts.LOGGER_NAME)


def __get_column_value(solutions: pd.DataFrame, index: int, column=None) -> str:
    return solutions[column].iloc[index]


# Todo: Replace to ati data class
def __get_ati_data(solutions: pd.DataFrame, index: int) -> tuple:
    timestamp = __get_column_value(solutions, index, consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value)
    event_type = __get_column_value(solutions, index, consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value)
    event_data = __get_column_value(solutions, index, consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value)
    return timestamp, event_type, event_data


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


def __parse_file(file: str, sg: SolutionGraph) -> SolutionGraph:
    log.info(f'Start solution space creating file {file}')
    solutions = pd.read_csv(file, encoding=consts.ISO_ENCODING)
    i = 0
    while i < solutions.shape[0]:
        date = __get_column_value(solutions, i, consts.CODE_TRACKER_COLUMN.DATE.value)
        timestamp = __get_column_value(solutions, i, consts.CODE_TRACKER_COLUMN.TIMESTAMP.value)
        fragment = __get_column_value(solutions, i, consts.CODE_TRACKER_COLUMN.FRAGMENT.value)
        i, ati_elements = __find_same_fragments(solutions, i)
        #Todo: create ast and run canonacalization process and modify sg
        pass
    return sg


def construct_solution_graph(path: str) -> SolutionGraph:
    files = get_all_file_system_items(path, csv_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    sg = SolutionGraph()
    for file in files:
        sg = __parse_file(file, sg)
        pass
    return sg