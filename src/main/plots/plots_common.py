import os
import logging

import pandas as pd
import matplotlib.pyplot as plt

from src.main.util.consts import EXTENSION
from src.main.util import consts
from src.main.plots import consts as plot_consts
from src.main.util.file_util import get_name_from_path, get_parent_folder_name, png_file_condition, remove_file, \
    ct_file_condition, change_extension_to, get_file_and_parent_folder_names, get_all_file_system_items

FRAGMENT_COL = consts.CODE_TRACKER_COLUMN.FRAGMENT.value
TIMESTAMP_COL = consts.CODE_TRACKER_COLUMN.TIMESTAMP.value
CHOSEN_TASK_COL = consts.CODE_TRACKER_COLUMN.CHOSEN_TASK.value
TASK_STATUS_COL = consts.CODE_TRACKER_COLUMN.TASK_STATUS.value
EVENT_TYPE_COL = consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value
EVENT_DATA_COL = consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value

log = logging.getLogger(consts.LOGGER_NAME)


def get_short_name(path: str):
    folder = get_parent_folder_name(path)
    file_name = get_name_from_path(path)
    return os.path.join(folder, file_name[:plot_consts.SHORT_NAME_LENGTH] + '...' + file_name[-plot_consts.SHORT_NAME_LENGTH:])


def save_plot(folder_to_save: str, data_path: str, fig: plt.figure, name_prefix: str):
    log.info('Saving' + data_path)
    name = name_prefix + '_' + (get_file_and_parent_folder_names(change_extension_to(data_path, EXTENSION.PNG.value)).replace('/', '_'))
    fig.savefig(os.path.join(folder_to_save, name), bbox_inches='tight')


# add fragments lengths to the plot
def add_fragments_length_plot(ax: plt.axes, data: pd.DataFrame):
    ax.scatter(data[TIMESTAMP_COL], data[plot_consts.FRAGMENT_LENGTH_COL],
               color=plot_consts.FRAGMENT_LENGTH_COLOR, s=plot_consts.SMALL_SIZE)


# to remove previously saved plots
def remove_all_png_files(root: str):
    files = get_all_file_system_items(root, png_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    for file in files:
        remove_file(file)


# these functions are useful to analyze data and find files to make plots based on them
def print_all_unique_values_in_file(file: str, column: str):
    data = pd.read_csv(file, encoding=consts.ISO_ENCODING)
    ati_events = data[column].dropna().unique().tolist()
    if ati_events:
        print(file)
        print(ati_events)


def print_all_unique_values_in_files(path: str, column: str):
    files = get_all_file_system_items(path, ct_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
    for file in files:
        print_all_unique_values_in_file(file, column)