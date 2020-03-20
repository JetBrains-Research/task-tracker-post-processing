# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

import pandas as pd
import matplotlib.pyplot as plt

from typing import List
from src.main.util import consts
from src.main.plots.util import consts as plot_consts
from src.main.plots.util.plots_common import get_short_name
from src.main.plots.util.pyplot_util import add_fragments_length_plot, EVENT_DATA_COL, TIMESTAMP_COL, FRAGMENT_COL, \
    save_and_show_if_needed, add_legend_to_the_right

log = logging.getLogger(consts.LOGGER_NAME)


def __create_ati_events_plot(ax: plt.axes, df: pd.DataFrame, event_data: List[str],
                             event_colors: dict, title: str) -> None:
    add_fragments_length_plot(ax, df)
    for event in event_data:
        event_df = df.loc[df[EVENT_DATA_COL] == event]
        add_fragments_length_plot(ax, event_df, event_colors[event], plot_consts.LARGE_SIZE, event)
    add_legend_to_the_right(ax)
    ax.set_ylabel(plot_consts.FRAGMENT_LENGTH_COL)
    ax.set_xlabel(TIMESTAMP_COL)
    ax.set_title(title)


# Create plots with different event types (running events and editor events), taken from ati data
def create_ati_data_plot(path: str, folder_to_save: str = None, to_show: bool = False) -> None:
    data = pd.read_csv(path, encoding=consts.ISO_ENCODING)
    data[plot_consts.FRAGMENT_LENGTH_COL] = data[FRAGMENT_COL].fillna('').str.len()

    fig, (ax_run, ax_editor) = plt.subplots(2, 1, figsize=(20, 10))
    run_title = f'Run events in {get_short_name(path)}'
    __create_ati_events_plot(ax_run, data, [e.value for e in plot_consts.ATI_RUN_EVENT],
                             plot_consts.ATI_RUN_EVENT_COLOR_DICT, run_title)

    editor_title = f'Editor events in {get_short_name(path)}'
    __create_ati_events_plot(ax_editor, data, [e.value for e in plot_consts.ATI_EDITOR_EVENT],
                             plot_consts.ATI_EDITOR_EVENT_COLOR_DICT, editor_title)

    save_and_show_if_needed(folder_to_save, to_show, fig, data_path=path, name_prefix='ati_events')
