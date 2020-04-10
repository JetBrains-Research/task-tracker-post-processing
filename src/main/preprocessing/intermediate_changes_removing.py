# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import pandas as pd
from typing import Optional

from src.main.util import consts
from src.main.util.consts import LOGGER_NAME, TMP_COLUMN
from src.main.util.data_util import handle_folder

log = logging.getLogger(LOGGER_NAME)

FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value
SHIFT_FRAGMENT = TMP_COLUMN.SHIFT_FRAGMENT.value
CHANGES = TMP_COLUMN.CHANGES.value
SHIFT_CHANGES = TMP_COLUMN.SHIFT_CHANGES.value


def __line_number_with_same_fragments(current_fragment: str, next_fragment: str) -> Optional[int]:
    # If one of the fragments is nan
    # Then changes were not in the same lines
    if consts.DEFAULT_VALUE.FRAGMENT.is_equal(current_fragment) \
            or consts.DEFAULT_VALUE.FRAGMENT.is_equal(next_fragment):
        return None

    current_fragment_lines = current_fragment.strip('\n').split('\n')
    next_fragment_lines = next_fragment.strip('\n').split('\n')
    # If fragments have the different number of lines
    # then changes were not in the same lines
    if len(current_fragment_lines) != len(next_fragment_lines):
        return None

    lines_with_diffs = []
    for i, (line_from_first, line_from_second) in enumerate(zip(current_fragment_lines, next_fragment_lines)):
        if line_from_first != line_from_second:
            lines_with_diffs.append(i)

    # If fragments have more than 1 lines with diffs,
    # then changes was not only in the same lines
    if len(lines_with_diffs) == 1:
        return lines_with_diffs[0]
    return None


def __remove_tmp_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in TMP_COLUMN:
        del df[column.value]
    return df


def __fill_changes_values(df: pd.DataFrame) -> pd.DataFrame:
    df[SHIFT_CHANGES] = df[CHANGES]
    df[CHANGES] = df[CHANGES].shift(-1)
    if df[CHANGES].iloc[0] is not None:
        df[SHIFT_CHANGES].iloc[0] = df[CHANGES].iloc[0]
    return df


def __remove_intermediate_changes_from_df(df: pd.DataFrame) -> pd.DataFrame:
    df[SHIFT_FRAGMENT] = df[FRAGMENT].shift(1)
    df[CHANGES] = df.apply(lambda row: __line_number_with_same_fragments(row[FRAGMENT], row[SHIFT_FRAGMENT]), axis=1)
    __fill_changes_values(df)
    df = df[df[CHANGES] != df[SHIFT_CHANGES]]
    __remove_tmp_columns(df)
    return df


def remove_intermediate_changes(path: str, result_folder_prefix: str = 'remove_inter_steps') -> str:
    return handle_folder(path, result_folder_prefix, __remove_intermediate_changes_from_df)
