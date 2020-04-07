# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import pandas as pd

from src.main.util import consts
from src.main.util.consts import LOGGER_NAME, ISO_ENCODING
from src.main.util.file_util import get_all_file_system_items, extension_file_condition, get_result_folder, write_result

log = logging.getLogger(LOGGER_NAME)


FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value


def __is_same_line_with_changes(current_fragment: str, next_fragment: str) -> bool:
    if consts.DEFAULT_VALUE.FRAGMENT.is_equal(current_fragment) \
            or consts.DEFAULT_VALUE.FRAGMENT.is_equal(next_fragment):
        return False

    current_fragment_lines = current_fragment.split('\n')
    next_fragment_lines = next_fragment.split('\n')
    # If fragments have the different number of lines
    # then changes was not in the same lines
    if len(current_fragment_lines) != len(next_fragment_lines):
        return False

    lines_with_diffs = set()
    for i, (line_from_first, line_from_second) in enumerate(zip(current_fragment_lines, next_fragment_lines)):
        if line_from_first != line_from_second:
            lines_with_diffs.add(i)

    # If fragments have more than 1 lines with diffs,
    # then changes was not only in the same lines
    return len(lines_with_diffs) == 1


def __get_next_line_index_with_changes(df: pd.DataFrame, index: int) -> int:
    while index < df.shape[0] - 1 and \
            __is_same_line_with_changes(df[FRAGMENT].iloc[index], df[FRAGMENT].iloc[index + 1]):
        index += 1
    return index


def __handle_df(df: pd.DataFrame) -> pd.DataFrame:
    i = 0
    need_to_remove = []
    while i < df.shape[0]:
        new_index = __get_next_line_index_with_changes(df, i)
        if new_index != i:
            need_to_remove += [_ for _ in range(i, new_index)]
        i = new_index + 1
    return df.drop(need_to_remove)


def remove_intermediate_steps(path: str, result_folder_prefix: str = 'remove_inter_steps') -> str:
    result_folder = get_result_folder(path, result_folder_prefix)
    files = get_all_file_system_items(path, extension_file_condition(consts.EXTENSION.CSV))
    for file in files:
        df = pd.read_csv(file, encoding=ISO_ENCODING)
        df = __handle_df(df)
        write_result(result_folder, path, file, df)
    return result_folder


remove_intermediate_steps('/Users/macbook/PycharmProjects/codetracker-data/1_test_sg/pies')