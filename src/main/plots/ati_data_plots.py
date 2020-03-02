import logging

import pandas as pd
import matplotlib.pyplot as plt

from src.main.util import consts
from src.main.plots import consts as plot_consts
from main.plots.plots_common import save_plot, add_fragments_length_plot, get_short_name, EVENT_DATA_COL, \
    TIMESTAMP_COL, FRAGMENT_COL

log = logging.getLogger(consts.LOGGER_NAME)


def __create_ati_events_plot(ax: plt.axes, df: pd.DataFrame, event_data: list, event_colors: dict, title: str):
    add_fragments_length_plot(ax, df)
    for event_data in event_data:
        event_data_df = df.loc[df[EVENT_DATA_COL] == event_data]
        ax.scatter(event_data_df[TIMESTAMP_COL], event_data_df[plot_consts.FRAGMENT_LENGTH_COL],
                   color=event_colors[event_data], s=plot_consts.LARGE_SIZE, label=event_data)
    ax.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)
    ax.set_ylabel(plot_consts.FRAGMENT_LENGTH_COL)
    ax.set_xlabel(TIMESTAMP_COL)
    ax.set_title(title)


# create plots with different event types (running events and editor events), taken from ati data
def create_ati_data_plot(path: str, folder_to_save=None, to_show=False):
    data = pd.read_csv(path, encoding=consts.ISO_ENCODING)
    data[plot_consts.FRAGMENT_LENGTH_COL] = data[FRAGMENT_COL].fillna('').str.len()

    fig, (ax_run, ax_editor) = plt.subplots(2, 1, figsize=(20, 10))
    run_title = f'run events in {get_short_name(path)}'
    __create_ati_events_plot(ax_run, data, [e.value for e in plot_consts.ATI_RUN_EVENT],
                             plot_consts.ATI_RUN_EVENT_COLOR_DICT, run_title)

    editor_title = f'editor events in {get_short_name(path)}'
    __create_ati_events_plot(ax_editor, data, [e.value for e in plot_consts.ATI_EDITOR_EVENT],
                             plot_consts.ATI_EDITOR_EVENT_COLOR_DICT, editor_title)

    if folder_to_save:
        save_plot(folder_to_save, path, fig, 'ati_events_')
    if to_show:
        log.info('Showing ' + path)
        fig.show()
