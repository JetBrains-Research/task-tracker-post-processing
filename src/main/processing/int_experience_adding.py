# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pandas as pd

from src.main.util.file_util import get_all_file_system_items, get_output_directory, write_result
from src.main.util.consts import ISO_ENCODING, TASK_TRACKER_COLUMN, INT_EXPERIENCE, DEFAULT_VALUE


def convert_to_int_experience(experience: str) -> int:
    try:
        int_experience = INT_EXPERIENCE[experience].value
        return int_experience
    except KeyError:
        return DEFAULT_VALUE.INT_EXPERIENCE.value


def add_int_experience(path: str, output_directory_prefix: str = 'int_exp') -> str:
    """
    This function allows to add the int experience column to the files. It can be useful if you need to sort the data
    by the users' experience. Int experience values can be found in the const file (the INT_EXPERIENCE Enum class).

    Note: It may be necessary for files with old data format

    For more details see
    https://github.com/JetBrains-Research/task-tracker-post-processing/wiki/Data-processing:-add-int-experience-column
    """
    output_directory = get_output_directory(path, output_directory_prefix)
    files = get_all_file_system_items(path)
    for file in files:
        df = pd.read_csv(file, encoding=ISO_ENCODING)
        if TASK_TRACKER_COLUMN.EXPERIENCE.value in df.columns:
            # It is old file structure
            df[TASK_TRACKER_COLUMN.INT_EXPERIENCE.value] = \
                df[TASK_TRACKER_COLUMN.EXPERIENCE.value].apply(convert_to_int_experience)
        write_result(output_directory, path, file, df)
    return output_directory
