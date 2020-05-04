# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Dict

import plotly
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.main.util import consts
from src.main.plots.util import consts as plot_consts
from src.main.util.file_util import change_extension_to
from src.main.plots.util.plots_common import create_directory_for_plots, get_readable_key
from src.main.plots.util.consts import STATISTICS_KEY, PLOTTY_CATEGORY_ORDER, STATISTICS_FREQ, STATISTICS_SHOWING_KEY, \
    STATISTICS_COLORS, PLOT_TYPE

log = logging.getLogger(consts.LOGGER_NAME)


def save_plot(fig: go.Figure, path: str, plot_type: plot_consts.PLOT_TYPE, plot_name: str = 'result_plot',
              format: consts.EXTENSION = consts.EXTENSION.HTML, auto_open: bool = False) -> None:
    file_name = create_directory_for_plots(path, plot_type.value, change_extension_to(plot_name, format))
    if format == consts.EXTENSION.HTML:
        plotly.offline.plot(fig, filename=file_name, auto_open=auto_open)
    else:
        # If you have an error during constructing plots, please install required dependencies:
        # https://plotly.com/python/static-image-export/
        fig.write_image(file_name)


def update_layout(fig: go.Figure, column: STATISTICS_KEY,
                  x_category_order: PLOTTY_CATEGORY_ORDER = PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING) -> go.Figure:
    # x_category_order='total ascending' means: in order of increasing values in Y
    # x_category_order='category ascending' means: in order of increasing values in X
    fig.update_layout(
        yaxis=dict(
            title_text=STATISTICS_SHOWING_KEY.FREQ.value
        ),
        xaxis=dict(
            title_text=get_readable_key(column.value),
            # We use type = 'category' because we want to display all values (numbers and strings)
            type='category',
            categoryorder=x_category_order.value
        ),
        plot_bgcolor=STATISTICS_COLORS.BAR_CHART_BG.value
    )
    return fig


def get_freq_bar_chart(statistics_df: pd.DataFrame, title: str, column: STATISTICS_KEY, labels: Dict[str, str],
                       x_category_order: PLOTTY_CATEGORY_ORDER = PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING,
                       to_update_layout: bool = True) -> go.Figure:
    fig = px.bar(statistics_df, x=column.value, y=STATISTICS_FREQ, title=title, labels=labels,
                 hover_data=[column.value, STATISTICS_FREQ])
    if to_update_layout:
        fig = update_layout(fig, column, x_category_order)
    fig.update_yaxes(automargin=True)
    return fig


def plot_freq_chart(statistics_df: pd.DataFrame, title: str, path: str, column: STATISTICS_KEY,
                    labels: Dict[str, str], plot_name: str, format: consts.EXTENSION = consts.EXTENSION.HTML,
                    auto_open: bool = False, plot_type: PLOT_TYPE = PLOT_TYPE.BAR,
                    x_category_order: PLOTTY_CATEGORY_ORDER = PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING) -> None:
    fig = get_freq_bar_chart(statistics_df, title, column, labels, x_category_order)
    save_plot(fig, path, plot_type, plot_name, format, auto_open)

