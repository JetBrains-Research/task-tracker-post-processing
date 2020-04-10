# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Tuple

import pandas as pd

from src.main.util import consts
from src.main.util.consts import LOGGER_NAME
from src.main.util.data_util import handle_folder

log = logging.getLogger(LOGGER_NAME)

FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value


def __is_same_line_with_changes(current_fragment: str, next_fragment: str) -> Tuple[bool, int]:
    index_line_with_changes = -1
    is_same_line_with_changes = False
    # If one of the fragments is nan
    # Then changes were not in the same lines
    if consts.DEFAULT_VALUE.FRAGMENT.is_equal(current_fragment) \
            or consts.DEFAULT_VALUE.FRAGMENT.is_equal(next_fragment):
        return is_same_line_with_changes, index_line_with_changes

    current_fragment_lines = current_fragment.strip('\n').split('\n')
    next_fragment_lines = next_fragment.strip('\n').split('\n')
    # If fragments have the different number of lines
    # then changes were not in the same lines
    if len(current_fragment_lines) != len(next_fragment_lines):
        return is_same_line_with_changes, index_line_with_changes

    lines_with_diffs = []
    for i, (line_from_first, line_from_second) in enumerate(zip(current_fragment_lines, next_fragment_lines)):
        if line_from_first != line_from_second:
            lines_with_diffs.append(i)

    # If fragments have more than 1 lines with diffs,
    # then changes was not only in the same lines
    is_same_line_with_changes = len(lines_with_diffs) == 1
    if is_same_line_with_changes:
        index_line_with_changes = lines_with_diffs[0]
    return is_same_line_with_changes, index_line_with_changes


def __is_the_same_line_next_and_through_one(current_and_next: Tuple[bool, int],
                                            next_fragment: str, through_one_fragment: str) -> bool:
    next_and_through_one = __is_same_line_with_changes(next_fragment, through_one_fragment)
    if next_and_through_one[0] and current_and_next[1] == next_and_through_one[1]:
        return True
    return False


def __handle_last_pair(current_fragment: str, next_fragment: str, index: int) -> int:
    current_and_next = __is_same_line_with_changes(current_fragment,next_fragment)
    if current_and_next[0]:
        index += 1
    return index


def __get_next_line_index_with_changes(df: pd.DataFrame, index: int) -> Tuple[int, bool]:
    to_continue = True
    to_remove_last_index = True
    while index < df.shape[0] - 2 and to_continue:
        current_and_next = __is_same_line_with_changes(df[FRAGMENT].iloc[index], df[FRAGMENT].iloc[index + 1])
        if current_and_next[0]:
            index += 1
            if not __is_the_same_line_next_and_through_one(current_and_next,
                                                           df[FRAGMENT].iloc[index],
                                                           df[FRAGMENT].iloc[index + 1]):
                to_remove_last_index = False
                to_continue = False
            index += 1
        else:
            to_continue = False

    if index == df.shape[0] - 2:
        index = __handle_last_pair(df[FRAGMENT].iloc[index], df[FRAGMENT].iloc[index + 1], index)

    return index, to_remove_last_index


def __remove_intermediate_changes_from_df(df: pd.DataFrame) -> pd.DataFrame:
    i = 0
    indices_to_remove = []
    while i < df.shape[0]:
        new_index, to_remove_last_index = __get_next_line_index_with_changes(df, i)
        if new_index != i:
            indices_to_remove += range(i, new_index - 1)
            if to_remove_last_index:
                indices_to_remove.append(new_index - 1)

        i = new_index + 1
    return df.drop(indices_to_remove)


def remove_intermediate_changes(path: str, result_folder_prefix: str = 'remove_inter_steps') -> str:
    return handle_folder(path, result_folder_prefix, __remove_intermediate_changes_from_df)
