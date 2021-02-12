# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pandas as pd
import numpy as np

from src.main.util import consts
from src.main.util.consts import FILE_SYSTEM_ITEM
from src.main.util.data_util import handle_folder
from src.main.util.file_util import get_all_file_system_items, language_item_condition, get_output_directory


FRAGMENT = consts.TASK_TRACKER_COLUMN.FRAGMENT.value
ROW_NUMBER = consts.TASK_TRACKER_COLUMN.ROW_NUMBER.value


def __filter_same_fragments(df: pd.DataFrame) -> pd.DataFrame:
    filtered_df = df.loc[df[FRAGMENT].shift(-1) != df[FRAGMENT]]
    filtered_df[ROW_NUMBER] = np.arange(filtered_df.shape[0])
    return filtered_df


def filter_same_fragments(path: str, output_directory_prefix: str = 'filter_same_fragments') -> str:
    """
    This function allows to delete consecutive same fragments and add column id with row number
    """
    languages = get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
    output_directory = get_output_directory(path, output_directory_prefix)
    for _ in languages:
        handle_folder(path, output_directory_prefix, __filter_same_fragments)
    return output_directory
