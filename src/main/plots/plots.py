import logging
import os

import pandas as pd
import matplotlib.pyplot as plt

from main.plots.consts import ATI_RUN_EVENT, ATI_RUN_EVENT_COLOR_DICT, ATI_EDITOR_EVENT, ATI_EDITOR_EVENT_COLOR_DICT, \
    TASK_COLOR_DICT, TASK_STATUS_COLOR_DICT, SMALL_SIZE, LARGE_SIZE, SHORT_NAME_LENGTH, FRAGMENT_LENGTH_COL, \
    FRAGMENT_LENGTH_COLOR
from src.main.util.strings_util import convert_camel_case_to_snake_case
from src.main.util.consts import ISO_ENCODING, LOGGER_NAME, CODE_TRACKER_COLUMN, TASK, \
    ACTIVITY_TRACKER_COLUMN, FILE_SYSTEM_ITEM, TASK_STATUS
from src.main.util.file_util import get_parent_folder, get_name_from_path, get_parent_folder_name, \
    get_all_file_system_items, png_file_condition, remove_file, ct_file_condition, change_extension_to


FRAGMENT_COL = CODE_TRACKER_COLUMN.FRAGMENT.value
TIMESTAMP_COL = CODE_TRACKER_COLUMN.TIMESTAMP.value
CHOSEN_TASK_COL = CODE_TRACKER_COLUMN.CHOSEN_TASK.value
TASK_STATUS_COL = CODE_TRACKER_COLUMN.TASK_STATUS.value
EVENT_TYPE_COL = ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value
EVENT_DATA_COL = ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value


log = logging.getLogger(LOGGER_NAME)


def __get_short_name(path: str):
    folder = get_parent_folder_name(path)
    file_name = get_name_from_path(path)
    folder_with_name = os.path.join(folder,  file_name[:SHORT_NAME_LENGTH] + '...' + file_name[-SHORT_NAME_LENGTH:])
    return folder_with_name


def __save_plot(path: str, fig: plt.figure, name_prefix: str):
    log.info('Saving' + path)
    name = name_prefix + '_' + get_name_from_path(change_extension_to(path, '.png'))
    fig.savefig(os.path.join(get_parent_folder(path), name), bbox_inches='tight')


# add fragments lengths to the plot
def __add_fragments_length_plot(ax: plt.axes, data: pd.DataFrame):
    ax.scatter(data[TIMESTAMP_COL], data[FRAGMENT_LENGTH_COL], color=FRAGMENT_LENGTH_COLOR, s=SMALL_SIZE)


# get x for original task splits according 'chosenTask' column
# make sure all tasks are written in snake case
def create_task_split_x_dict(data: pd.DataFrame):
    task_split_x_dict = {}
    for task in TASK:
        task_split_x_dict[task.value] = data.loc[data[CHOSEN_TASK_COL] == task.value][TIMESTAMP_COL]
    return task_split_x_dict


# get x for original task status according 'taskStatus' column
# make sure all tasks are written in snake case
def create_status_x_dict(data: pd.DataFrame):
    status_x_dict = {}
    for status in TASK_STATUS:
        status_x_dict[status.value] = data.loc[data[TASK_STATUS_COL] == status.value][TIMESTAMP_COL]
    return status_x_dict


# show plot with changes of code fragments size, colored according to 'chosenTask' field
def show_colored_splits_plot(path: str, task_split_x_dict=None, status_x_dict=None, to_save=False, to_snake_case=True):
    data = pd.read_csv(path, encoding=ISO_ENCODING)
    data[FRAGMENT_LENGTH_COL] = data[FRAGMENT_COL].fillna('').str.len()

    if to_snake_case:
        data[CHOSEN_TASK_COL] = data[CHOSEN_TASK_COL].fillna('').apply(lambda t: convert_camel_case_to_snake_case(t))
    if not task_split_x_dict:
        task_split_x_dict = create_task_split_x_dict(data)
    if not status_x_dict:
        status_x_dict = create_status_x_dict(data)
    fig, ax = plt.subplots(figsize=(10, 5))

    # add colored background to the plot
    max_fragment_length = data[FRAGMENT_LENGTH_COL].max()
    for task in TASK:
        ax.fill_between(task_split_x_dict[task.value],
                        0,
                        max_fragment_length,
                        color=TASK_COLOR_DICT[task.value],
                        label=task.value)

    __add_fragments_length_plot(ax, data)
    
    # add task status to the plot
    for status in TASK_STATUS:
       ax.scatter(status_x_dict[status.value],
                  data.loc[data.index.isin(status_x_dict[status.value].index)][FRAGMENT_LENGTH_COL],
                  color=TASK_STATUS_COLOR_DICT[status.value],
                  label=status.value.lower(),
                  s=LARGE_SIZE)

    ax.legend(bbox_to_anchor=(1.04,1), borderaxespad=0)

    plt.xlabel(TIMESTAMP_COL)
    plt.ylabel(FRAGMENT_LENGTH_COL)
    plt.title(__get_short_name(path))

    if to_save:
        __save_plot(path, fig, 'split_')
    log.info('Showing ' + path)
    fig.show()


def __create_ati_events_plot(ax: plt.axes, df: pd.DataFrame, event_data: list, event_colors: dict, title: str):
    __add_fragments_length_plot(ax, df)
    for event_data in event_data:
        event_data_df = df.loc[df[EVENT_DATA_COL] == event_data]
        ax.scatter(event_data_df[TIMESTAMP_COL], event_data_df[FRAGMENT_LENGTH_COL],
                   color=event_colors[event_data], s=LARGE_SIZE, label=event_data)
    ax.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)
    ax.set_ylabel(FRAGMENT_LENGTH_COL)
    ax.set_xlabel(TIMESTAMP_COL)
    ax.set_title(title)


def __print_all_unique_values_in_file(file: str, column: str):
    data = pd.read_csv(file, encoding=ISO_ENCODING)
    ati_events = data[column].dropna().unique().tolist()
    if ati_events:
        print(file)
        print(ati_events)


def __print_all_unique_values_in_files(path: str, column: str):
    files = get_all_file_system_items(path, ct_file_condition, FILE_SYSTEM_ITEM.FILE.value)
    for file in files:
        __print_all_unique_values_in_file(file, column)


# todo: add 'CompilationFinished' event?
#  now there are only 'Action' events, but i cannot find any events of this type in our data
def show_ati_data_plot(path: str, to_save=False):
    data = pd.read_csv(path, encoding=ISO_ENCODING)
    data[FRAGMENT_LENGTH_COL] = data[FRAGMENT_COL].fillna('').str.len()

    fig, (ax_run, ax_editor) = plt.subplots(2, 1, figsize=(20, 10))
    run_title = f'run events in {__get_short_name(path)}'
    __create_ati_events_plot(ax_run, data, [e.value for e in ATI_RUN_EVENT], ATI_RUN_EVENT_COLOR_DICT, run_title)

    editor_title = f'editor events in {__get_short_name(path)}'
    __create_ati_events_plot(ax_editor, data, [e.value for e in ATI_EDITOR_EVENT], ATI_EDITOR_EVENT_COLOR_DICT, editor_title)

    if to_save:
        __save_plot(path, fig, 'ati_events_')
    log.info('Showing ' + path)
    fig.show()


# to remove previously saved plots
def remove_all_png_files(root: str):
    files = get_all_file_system_items(root, png_file_condition, FILE_SYSTEM_ITEM.FILE.value)
    for file in files:
        remove_file(file)
