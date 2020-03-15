# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

import pandas as pd
import matplotlib.pyplot as plt

from src.main.util import consts
from src.main.plots.util import consts as plot_consts
from src.main.splitting.splitting import find_splits
from src.main.plots.util.plots_common import get_short_name
from src.main.util.file_util import get_name_from_path
from src.main.util.strings_util import convert_camel_case_to_snake_case
from src.main.plots.util.pyplot_util import CHOSEN_TASK_COL, TIMESTAMP_COL, TASK_STATUS_COL, FRAGMENT_COL, \
    add_fragments_length_plot, save_and_show_if_needed, add_legend_to_the_right


log = logging.getLogger(consts.LOGGER_NAME)


# get x for original task splits according 'chosenTask' column
# make sure all tasks are written in snake case
def __create_task_split_x_dict(data: pd.DataFrame):
    task_split_x_dict = {}
    for task in consts.TASK:
        task_split_x_dict[task.value] = data.loc[data[CHOSEN_TASK_COL] == task.value][TIMESTAMP_COL]
    return task_split_x_dict


# get x for original task status according 'taskStatus' column
# make sure all tasks are written in snake case
def __create_status_x_dict(data: pd.DataFrame):
    status_x_dict = {}
    for status in consts.TASK_STATUS:
        status_x_dict[status.value] = data.loc[data[TASK_STATUS_COL] == status.value][TIMESTAMP_COL]
    return status_x_dict


def __add_tasks_colored_background(ax: plt.axes, data: pd.DataFrame, task_split_x_dict=None):
    if not task_split_x_dict:
        task_split_x_dict = __create_task_split_x_dict(data)
    max_length = data[plot_consts.FRAGMENT_LENGTH_COL].max()
    for task in consts.TASK.tasks():
        ax.fill_between(task_split_x_dict[task], 0, max_length, color=plot_consts.TASK_COLOR_DICT[task],label=task)


def __add_task_status_to_plot(ax: plt.axes, data: pd.DataFrame, status_x_dict=None):
    if not status_x_dict:
        status_x_dict = __create_status_x_dict(data)
    for status in consts.TASK_STATUS:
        ax.scatter(status_x_dict[status.value],
                   data.loc[data.index.isin(status_x_dict[status.value].index)][plot_consts.FRAGMENT_LENGTH_COL],
                   color=plot_consts.TASK_STATUS_COLOR_DICT[status.value],
                   label=status.value.lower(),
                   s=plot_consts.LARGE_SIZE)


def __create_splitting_plot(ax: plt.axes, data: pd.DataFrame, title: str,
                            task_split_x_dict=None, status_x_dict=None, to_snake_case=True):
    data[plot_consts.FRAGMENT_LENGTH_COL] = data[FRAGMENT_COL].fillna('').str.len()
    if to_snake_case:
        data[CHOSEN_TASK_COL] = data[CHOSEN_TASK_COL].fillna('').apply(lambda t: convert_camel_case_to_snake_case(t))

    # add colored background to the plot
    __add_tasks_colored_background(ax, data, task_split_x_dict)

    # add fragments length plot
    add_fragments_length_plot(ax, data)

    # add task status to the plot
    __add_task_status_to_plot(ax, data, status_x_dict)

    add_legend_to_the_right(ax)
    ax.set_xlabel(TIMESTAMP_COL)
    ax.set_ylabel(plot_consts.FRAGMENT_LENGTH_COL)
    ax.set_title(title)


def __create_comparative_plot(first_df: pd.DataFrame, second_df: pd.DataFrame, first_title: str, second_title: str,
                              data_path=None, folder_to_save=None, name_prefix='', to_snake_case=True, to_show=False):
    fig, (ax, second_df_ax) = plt.subplots(2, 1, figsize=(20, 10))
    __create_splitting_plot(ax, first_df, first_title, to_snake_case=to_snake_case)
    __create_splitting_plot(second_df_ax, second_df, second_title, to_snake_case=to_snake_case)

    save_and_show_if_needed(folder_to_save, to_show, fig, data_path=data_path, name_prefix=name_prefix)


# show plot with changes of code fragments size, colored according to 'chosenTask' field before and after finding splits
# to_snake_case is needed for correct tasks splits showing
def create_comparative_splitting_plot(data_path: str, to_snake_case=True, folder_to_save=None, to_show=False):
    original_splits_data = pd.read_csv(data_path, encoding=consts.ISO_ENCODING)
    original_splits_title = f'{get_short_name(data_path)} with original splits'

    real_splits_data = find_splits(original_splits_data.copy())
    real_splits_title = f'{get_short_name(data_path)} with real splits'

    __create_comparative_plot(original_splits_data, real_splits_data, original_splits_title, real_splits_title,
                              data_path, folder_to_save, 'split', to_snake_case, to_show)


def create_comparative_filtering_plot(original_data_path: str, filtered_data_path: str,
                                      to_snake_case=True, folder_to_save=None, to_show=False):
    original_data = pd.read_csv(original_data_path, encoding=consts.ISO_ENCODING)
    original_data_title = f'Original data {get_short_name(original_data_path)}'

    filtered_data_data = pd.read_csv(filtered_data_path, encoding=consts.ISO_ENCODING)
    filtered_data_title = f'Filtered data {get_short_name(filtered_data_path)}'

    result_name_prefix = 'comparative_filtering_' + get_short_name(get_name_from_path(original_data_path))

    __create_comparative_plot(original_data, filtered_data_data, original_data_title, filtered_data_title,
                              folder_to_save=folder_to_save, to_snake_case=to_snake_case, to_show=to_show,
                              name_prefix=result_name_prefix)

