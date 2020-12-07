# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

from src.main.plots.util.consts import CT_SECONDS_COL
from src.main.util import consts
from src.main.plots.util import consts as plot_consts
from src.main.plots.util.plots_common import get_result_file_name

FRAGMENT_COL = consts.TASK_TRACKER_COLUMN.FRAGMENT.value
TIMESTAMP_COL = consts.TASK_TRACKER_COLUMN.TIMESTAMP.value
CHOSEN_TASK_COL = consts.TASK_TRACKER_COLUMN.CHOSEN_TASK.value
TASK_STATUS_COL = consts.TASK_TRACKER_COLUMN.TASK_STATUS.value
EVENT_TYPE_COL = consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value
EVENT_DATA_COL = consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value

log = logging.getLogger(consts.LOGGER_NAME)


def save_plot(folder_to_save: str, fig: plt.figure, name_prefix: str, data_path: Optional[str] = None,
              extension: consts.EXTENSION = consts.EXTENSION.PNG) -> None:
    name = get_result_file_name(name_prefix, data_path, extension)
    log.info('Saving ' + name)
    # 'tight' is used to alter the size of the bounding box (whitespace) around the output image
    fig.savefig(os.path.join(folder_to_save, name), bbox_inches='tight')


# Add fragments lengths to the plot
def add_fragments_length_plot(ax: plt.axes, data: pd.DataFrame, color: str = plot_consts.FRAGMENT_LENGTH_COLOR,
                              s: int = plot_consts.SMALL_SIZE, label: Optional[str] = None,
                              to_connect: bool = False) -> None:
    ax.scatter(data[CT_SECONDS_COL], data[plot_consts.FRAGMENT_LENGTH_COL], color=color, s=s, label=label)
    if to_connect:
        ax.plot(data[CT_SECONDS_COL], data[plot_consts.FRAGMENT_LENGTH_COL])


def add_legend_to_the_right(ax: plt.axes) -> None:
    # borderaxespad is the pad between the axes and legend border.
    # bbox_to_anchor sets coordinates of legend's corners
    ax.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)


def save_and_show_if_needed(folder_to_save: str, to_show: bool, fig: plt.figure, data_path: Optional[str] = None,
                            name_prefix: str = '') -> None:
    if folder_to_save:
        save_plot(folder_to_save, fig, name_prefix, data_path)
    if to_show:
        log.info('Showing ' + data_path)
        fig.show()
