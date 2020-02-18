import logging

import pandas as pd
import matplotlib.pyplot as plt

from main.plots import consts
from src.main.plots.consts import SHORT_NAME_LENGTH
from src.main.util.consts import ISO_ENCODING, LOGGER_NAME, CODE_TRACKER_COLUMN
from src.main.util.file_util import get_parent_folder, get_file_name_from_path, get_parent_folder_name

log = logging.getLogger(LOGGER_NAME)


def get_short_name(path):
    folder = get_parent_folder_name(path)
    file_name = get_file_name_from_path(path)
    folder_with_name = folder + '/' + file_name[:SHORT_NAME_LENGTH] + '...' + file_name[-SHORT_NAME_LENGTH:]
    return folder_with_name


def add_splits_on_plot(splits):
    for s in splits:
        plt.axvline(x=s, color='k', linestyle='-')


def get_status_color_size(f):
    return consts.STATUS_COLOR_SIZE_DICT.get(f, consts.STATUS_COLOR_SIZE_DEFAULT)


def get_task_color(t):
    return consts.TASK_COLOR_DICT.get(t, consts.TASK_COLOR_DEFAULT)


# show plot with changes of code fragments size, colored according to 'chosenTask' field
def show_colored_fragment_size_plot_with_splits(path, to_save=False, splits=None):
    if splits is None:
        splits = []
    data = pd.read_csv(path, encoding=ISO_ENCODING)

    fig, ax = plt.subplots()

    # Color depends on the task status: solved or not solved
    fragment_color_size = data[CODE_TRACKER_COLUMN.TASK_STATUS.value].apply(get_status_color_size)
    fragment_sizes = data[CODE_TRACKER_COLUMN.FRAGMENT.value].str.len()

    # Color depends on the current chosen task
    task_color = data[CODE_TRACKER_COLUMN.CHOSEN_TASK.value].apply(get_task_color)
    task_y = -1

    for i in range(len(fragment_sizes)):
        ax.plot(i, fragment_sizes[i], fragment_color_size[i][0], ms=fragment_color_size[i][1])
        ax.plot(i, task_y, task_color[i])

    plt.xlabel("change number")
    plt.ylabel("fragment size")
    plt.title(get_short_name(path))

    add_splits_on_plot(splits)

    if to_save:
        log.info("Saving" + path)
        fig.savefig(get_parent_folder(path, True) + "split_" + get_file_name_from_path(path, False) + ".png")

    log.info("Showing " + path)
    fig.show()
