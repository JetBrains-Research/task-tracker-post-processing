# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pandas as pd

from src.main.util import consts
from src.main.util.consts import FILE_SYSTEM_ITEM
from src.main.util.data_util import handle_folder
from src.main.util.file_util import get_all_file_system_items, language_item_condition, get_output_directory


def __delete_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols_to_keep = [consts.TASK_TRACKER_COLUMN.FRAGMENT.value,
                    consts.TASK_TRACKER_COLUMN.AGE.value,
                    consts.TASK_TRACKER_COLUMN.EXPERIENCE.value,
                    consts.TASK_TRACKER_COLUMN.TESTS_RESULTS.value,
                    consts.TASK_TRACKER_COLUMN.TASK.value]
    return df.loc[:, cols_to_keep]


def delete_unnecessary_columns(path: str, output_directory_prefix: str = 'delete_unnecessary_columns') -> str:
    """
    This function allows to delete columns that are not needed to build the solution
    space in the coding assistant project.

    After executing the function, only the next columns will remain:
    [FRAGMENT, AGE, EXPERIENCE, TEST_RESULT, TASK]
    """
    languages = get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
    output_directory = get_output_directory(path, output_directory_prefix)
    for _ in languages:
        handle_folder(path, output_directory_prefix, __delete_unnecessary_columns)
    return output_directory
