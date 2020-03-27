# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from typing import Optional

import pandas as pd

from src.main.util.strings_util import crop_string
from src.main.plots.util import consts as plot_consts
from src.main.util.consts import EXTENSION, DEFAULT_VALUE, INVALID_FILE_FOR_PREPROCESSING
from src.main.util.file_util import get_parent_folder_name, get_name_from_path, create_directory, get_parent_folder, \
    get_file_and_parent_folder_names, change_extension_to


def get_result_file_name(name_prefix: str, data_path: Optional[str] = None, extension: EXTENSION = EXTENSION.PNG) -> str:
    if data_path:
        name_prefix += '_' + (get_file_and_parent_folder_names(data_path).replace('/', '_'))
    return change_extension_to(name_prefix, extension)


def get_short_name(path: str) -> str:
    folder = get_parent_folder_name(path)
    file_name = get_name_from_path(path)
    return os.path.join(folder, crop_string(file_name, plot_consts.SHORT_NAME_LENGTH))


def to_filter_rare_values(statistics_df: pd.DataFrame) -> bool:
    return statistics_df[plot_consts.STATISTICS_FREQ] <= plot_consts.STATISTICS_RARE_VALUE_THRESHOLD


def create_directory_for_plots(path: str, folder: plot_consts.PLOT_TYPE, file_name: str,
                               statistics_folder_name: str = 'statistics') -> str:
    path = os.path.join(get_parent_folder(path), statistics_folder_name, str(folder))
    create_directory(path)
    return os.path.join(path, file_name)


# Get key, which will be shown on a plot
def get_readable_key(key: str, default_value: Optional[DEFAULT_VALUE] = None) -> str:
    # It was an incorrect file
    if key == str(INVALID_FILE_FOR_PREPROCESSING):
        return plot_consts.STATISTICS_SHOWING_KEY.INCORRECT.value
    # It was not indicated
    if key == str(default_value):
        return plot_consts.STATISTICS_SHOWING_KEY.NOT_INDICATED.value
    return key.replace('_', ' ').capitalize()


