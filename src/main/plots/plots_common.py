import os
import pandas as pd

from src.main.util import consts
from src.main.plots import consts as plot_consts
from src.main.util.strings_util import crop_string
from src.main.util.file_util import get_parent_folder_name, get_name_from_path, create_directory, get_parent_folder


def get_short_name(path: str):
    folder = get_parent_folder_name(path)
    file_name = get_name_from_path(path)
    return os.path.join(folder, crop_string(file_name, plot_consts.SHORT_NAME_LENGTH))


def filter_rare_values(statistics_df: pd.DataFrame):
    return statistics_df[plot_consts.STATISTIC_FREQ] <= plot_consts.STATISTICS_RARE_VALUE_THRESHOLD


def create_directory_for_plots(path: str, folder: plot_consts.PLOT_TYPES, file_name: str,
                               statistics_folder_name='statistics'):
    path = os.path.join(get_parent_folder(path), statistics_folder_name, str(folder))
    create_directory(path)
    return os.path.join(path, file_name)


# Get key, which will be shown on a plot
def get_readable_key(key: str, default_value=None):
    # It was an incorrect file
    if key == str(consts.INVALID_FILE_FOR_PREPROCESSING):
        return plot_consts.STATISTICS_SHOWING_KEY.INCORRECT.value
    # It was not indicated
    if key == str(default_value):
        return plot_consts.STATISTICS_SHOWING_KEY.NOT_INDICATED.value
    return key.replace('_', ' ').capitalize()


