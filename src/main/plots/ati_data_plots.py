# Copyright (c) by anonymous author(s)

import logging
from typing import List, Union, Dict

import pandas as pd
import matplotlib.pyplot as plt

from src.main.util import consts
from src.main.plots.util.plots_common import get_short_name, fill_seconds_columns
from src.main.plots.util.consts import FRAGMENT_LENGTH_COL, ATI_RUN_EVENT, ATI_EDITOR_EVENT_COLOR_DICT, LARGE_SIZE, \
    ATI_EDITOR_EVENT, ATI_RUN_EVENT_COLOR_DICT, CT_SECONDS_COL
from src.main.plots.util.pyplot_util import add_fragments_length_plot, EVENT_DATA_COL, TIMESTAMP_COL, FRAGMENT_COL, \
    save_and_show_if_needed, add_legend_to_the_right


log = logging.getLogger(consts.LOGGER_NAME)

AtiEvent = Union[ATI_RUN_EVENT, ATI_EDITOR_EVENT]


def __create_ati_events_plot(ax: plt.axes, df: pd.DataFrame, event_data: List[AtiEvent],
                             event_colors: Dict[AtiEvent, str], title: str) -> None:
    add_fragments_length_plot(ax, df)
    for event in event_data:
        event_df = df.loc[df[EVENT_DATA_COL] == event.value]
        add_fragments_length_plot(ax, event_df, event_colors[event], LARGE_SIZE, event.value)
    add_legend_to_the_right(ax)
    ax.set_ylabel(FRAGMENT_LENGTH_COL)
    ax.set_xlabel(CT_SECONDS_COL)
    ax.set_title(title)


# Create plots with different event types (running events and editor events), taken from ati data
def create_ati_data_plot(path: str, folder_to_save: str = None, to_show: bool = False) -> None:
    data = pd.read_csv(path, encoding=consts.ISO_ENCODING)
    fill_seconds_columns(data)
    data[FRAGMENT_LENGTH_COL] = data[FRAGMENT_COL].fillna('').str.len()

    fig, (ax_run, ax_editor) = plt.subplots(2, 1, figsize=(20, 10))
    run_title = f'Run events in {get_short_name(path)}'
    __create_ati_events_plot(ax_run, data, ATI_RUN_EVENT.get_events(), ATI_RUN_EVENT_COLOR_DICT, run_title)

    editor_title = f'Editor events in {get_short_name(path)}'
    __create_ati_events_plot(ax_editor, data, ATI_EDITOR_EVENT.get_events(), ATI_EDITOR_EVENT_COLOR_DICT, editor_title)

    save_and_show_if_needed(folder_to_save, to_show, fig, data_path=path, name_prefix='ati_events')

