# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Optional

import pandas as pd
from pandas import isna

from src.main.util import consts
from src.main.util.data_util import handle_folder
from src.main.util.consts import LOGGER_NAME, TMP_COLUMN, FILE_SYSTEM_ITEM
from src.main.util.file_util import get_all_file_system_items, language_item_condition, get_output_directory

log = logging.getLogger(LOGGER_NAME)

FRAGMENT = consts.TASK_TRACKER_COLUMN.FRAGMENT.value
SHIFTED_FRAGMENT = TMP_COLUMN.SHIFTED_FRAGMENT.value
DIFFS = TMP_COLUMN.DIFFS.value
SHIFTED_DIFFS = TMP_COLUMN.SHIFTED_DIFFS.value


# Returns a line number with diffs if there were diffs in only one line, and None otherwise
def __get_diffs_line_number(current_fragment: str, next_fragment: str) -> Optional[int]:
    # If one of the fragments is nan
    # Then diffs were not in the same lines
    if isna(current_fragment) or isna(next_fragment):
        return None

    current_fragment_lines = current_fragment.strip('\n').split('\n')
    next_fragment_lines = next_fragment.strip('\n').split('\n')
    # If fragments have the different number of lines
    # then diffs were not in the same lines
    if len(current_fragment_lines) != len(next_fragment_lines):
        return None

    line_indices_with_diffs = []
    for i, (line_from_first, line_from_second) in enumerate(zip(current_fragment_lines, next_fragment_lines)):
        if line_from_first != line_from_second:
            line_indices_with_diffs.append(i)

    # If fragments have more than 1 line with diffs,
    # then diffs were not only in the same lines
    if len(line_indices_with_diffs) == 1:
        return line_indices_with_diffs[0]
    return None


def __remove_tmp_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in TMP_COLUMN:
        del df[column.value]
    return df


def __fill_diffs_column(df: pd.DataFrame) -> pd.DataFrame:
    df[SHIFTED_DIFFS] = df[DIFFS]
    df[DIFFS] = df[DIFFS].shift(-1)
    if df[DIFFS].iloc[0] is not None:
        df[SHIFTED_DIFFS].iloc[0] = df[DIFFS].iloc[0]
    return df


def remove_intermediate_diffs_from_df(df: pd.DataFrame) -> pd.DataFrame:
    df[SHIFTED_FRAGMENT] = df[FRAGMENT].shift(1)
    df[DIFFS] = df.apply(lambda row: __get_diffs_line_number(row[FRAGMENT], row[SHIFTED_FRAGMENT]), axis=1)
    __fill_diffs_column(df)
    df = df[df[DIFFS] != df[SHIFTED_DIFFS]]
    __remove_tmp_columns(df)
    return df


def remove_intermediate_diffs(path: str, output_directory_prefix: str = 'remove_intermediate_diffs') -> str:
    """
    This function allows to remove intermediate diffs in the files. This means deleting all intermediate code snapshots
    that are collected during the writing of a code fragment.

    For example, if we have three consecutive snapshots:

    ...
    prin
    print
    print(5)
    ...

    we would like to delete the first 2 fragments because these are not final states.
    The final state is a completed line entered by the user.

    For more details see
    https://github.com/JetBrains-Research/task-tracker-post-processing/wiki/Data-processing:-remove-intermediate-diffs
    """
    languages = get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
    output_directory = get_output_directory(path, output_directory_prefix)
    for _ in languages:
        handle_folder(path, output_directory_prefix, remove_intermediate_diffs_from_df)
    return output_directory
