# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pandas as pd

from src.main.util import consts
from src.main.util.consts import FILE_SYSTEM_ITEM
from src.main.util.data_util import handle_folder
from src.main.util.file_util import get_all_file_system_items, language_item_condition, get_output_directory


TESTS_RESULT = consts.TASK_TRACKER_COLUMN.TESTS_RESULTS.value


def __filter_incorrect_fragments(df: pd.DataFrame) -> pd.DataFrame:
    return df[df[TESTS_RESULT] != -1]


def filter_incorrect_fragments(path: str, output_directory_prefix: str = 'filter_incorrect_fragments') -> str:
    """
    This function allows to filter incorrect fragments.
    The fragment is incorrect if the TESTS_RESULT column value is -1
    """
    languages = get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
    output_directory = get_output_directory(path, output_directory_prefix)
    for _ in languages:
        handle_folder(path, output_directory_prefix, __filter_incorrect_fragments)
    return output_directory
