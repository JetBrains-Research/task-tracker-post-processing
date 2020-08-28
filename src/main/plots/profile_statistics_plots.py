# Copyright (c) by anonymous author(s)

import logging
from typing import Dict, Any, List, Optional

import pandas as pd
import numpy as np
import plotly.express as px

from src.main.preprocessing.int_experience_adding import convert_to_int_experience
from src.main.util import consts
from src.main.util.consts import INT_EXPERIENCE, EXPERIENCE
from src.main.util.log_util import log_and_raise_error
from src.main.plots.util.plotly_util import save_plot, plot_and_save_freq_chart
from src.main.util.file_util import get_parent_folder, deserialize_data_from_file
from src.main.plots.util.plots_common import to_filter_rare_values, get_readable_key, get_labels_for_freq_plots
from src.main.plots.util.consts import PLOTTY_CATEGORY_ORDER, CHART_TYPE, STATISTICS_FREQ, STATISTICS_SHOWING_KEY, \
    STATISTICS_KEY, STATISTICS_COLORS

log = logging.getLogger(consts.LOGGER_NAME)


def __read_statistics_from_file(path: str, default_value: consts.DEFAULT_VALUE, column: STATISTICS_KEY) -> Dict[str, Any]:
    statistics_dict = deserialize_data_from_file(path)
    readable_statistics_dict = {}
    keys = statistics_dict.keys()
    # Sort by my order
    if column == STATISTICS_KEY.EXPERIENCE:
        keys = __sort_experience_keys(keys)
    for key in keys:
        readable_statistics_dict[__get_readable_key_specific_by_column(key, default_value, column)] = statistics_dict[key]
    return readable_statistics_dict


def __sort_experience_keys(keys: List[str]) -> List[str]:
    experiences_keys = [x for x in EXPERIENCE.sorted_values() if x in keys]
    experiences_keys += [x for x in keys if x not in experiences_keys]
    return experiences_keys


def __get_readable_key_specific_by_column(key: str, default_value: consts.DEFAULT_VALUE, column: STATISTICS_KEY) -> str:
    if column == STATISTICS_KEY.EXPERIENCE:
        try:
            return INT_EXPERIENCE[key].get_short_str()
        except KeyError:
            return get_readable_key(key, default_value)
    return get_readable_key(key, default_value)


def __get_statistics_df_from_file(path: str, column: STATISTICS_KEY, default_value: consts.DEFAULT_VALUE,
                                  to_union_rare: bool = False) -> pd.DataFrame:
    statistics_dict = __read_statistics_from_file(path, default_value, column)
    statistics_df = pd.DataFrame(statistics_dict.items(), columns=[column.value, STATISTICS_FREQ])
    # If we want to union rare values
    if to_union_rare:
        to_filter_series = to_filter_rare_values(statistics_df)
        statistics_df.loc[to_filter_series, column.value] \
            = [STATISTICS_SHOWING_KEY.OTHERS.value] * to_filter_series.size
    return statistics_df


def __get_title_for_plots(column: STATISTICS_KEY) -> str:
    return get_readable_key(column.value) + ' distribution'


def __plot_pie_chart(statistics_df: pd.DataFrame, title: str, path: str, column: STATISTICS_KEY,
                     labels: Dict[str, str], plot_name: str = 'distribution_plot',
                     format: consts.EXTENSION = consts.EXTENSION.HTML, auto_open: bool = False) -> None:
    fig = px.pie(statistics_df, values=STATISTICS_FREQ, names=column.value, title=title,
                 color_discrete_sequence=STATISTICS_COLORS.PIE_CHART.value,
                 hover_data=[STATISTICS_FREQ],
                 labels=labels)
    fig.update_traces(textposition='inside', textinfo='percent')
    save_plot(fig, path, CHART_TYPE.PIE, plot_name, format, auto_open)


def plot_profile_statistics(file: str, column: STATISTICS_KEY, plot_type: CHART_TYPE, to_union_rare: bool = False,
                            format: consts.EXTENSION = consts.EXTENSION.HTML, auto_open: bool = False,
                            x_category_order: PLOTTY_CATEGORY_ORDER = PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING,
                            x_axis_title: Optional[str] = None, y_axis_title: Optional[str] = None,
                            to_add_percents: bool = False, to_add_title: bool = True) -> None:
    default_value = column.get_default()
    statistics_df = __get_statistics_df_from_file(file, column, default_value, to_union_rare)
    path = get_parent_folder(file)
    labels = get_labels_for_freq_plots(column)
    title = __get_title_for_plots(column) if to_add_title else None
    if plot_type == CHART_TYPE.PIE:
        __plot_pie_chart(statistics_df, title, path, column, labels, plot_name=column.value, format=format,
                         auto_open=auto_open)
    elif plot_type == CHART_TYPE.BAR:
        plot_and_save_freq_chart(statistics_df, title, path, column, labels, plot_name=column.value, format=format,
                                 auto_open=auto_open, x_category_order=x_category_order, x_axis_title=x_axis_title,
                                 y_axis_title=y_axis_title, to_add_percents=to_add_percents)
    else:
        log_and_raise_error(f'Plot type {plot_type} is incorrect!', log)
