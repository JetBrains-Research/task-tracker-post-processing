# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import pandas as pd
import plotly.express as px


from src.main.util import consts
from src.main.plots import consts as plot_consts
from src.main.plots.plotly_util import save_plot
from src.main.plots.plots_common import filter_rare_values, get_readable_key
from src.main.util.file_util import get_parent_folder, deserialize_data_from_file


log = logging.getLogger(consts.LOGGER_NAME)


def __read_statistics_from_file(path: str, default_value: consts.DEFAULT_VALUES):
    statistics_dict = deserialize_data_from_file(path)
    readable_statistics_dict = {}
    for key in statistics_dict.keys():
        readable_statistics_dict[get_readable_key(key, default_value)] = statistics_dict[key]
    return readable_statistics_dict


def __get_statistics_df_from_file(path: str, column: plot_consts.STATISTICS_KEY, default_value: consts.DEFAULT_VALUES,
                                  to_union_rare=False):
    statistics_dict = __read_statistics_from_file(path, default_value)
    statistics_df = pd.DataFrame(statistics_dict.items(), columns=[column, plot_consts.STATISTICS_FREQ])
    # If we want to union rare values
    if to_union_rare:
        statistics_df.loc[filter_rare_values(statistics_df), column] = plot_consts.STATISTICS_SHOWING_KEY.OTHERS.value
    return statistics_df


def __get_labels_for_plots(column: plot_consts.STATISTICS_KEY):
    return {
        plot_consts.STATISTICS_FREQ: plot_consts.STATISTICS_SHOWING_KEY.FREQ.value,
        column: get_readable_key(str(column))
    }


def __get_title_for_plots(column: plot_consts.STATISTICS_KEY):
    return get_readable_key(str(column)) + ' distribution'


def __get_default_value_for_plots(column: plot_consts.STATISTICS_KEY):
    if column == plot_consts.STATISTICS_KEY.AGE.value:
        return consts.DEFAULT_VALUES.AGE.value
    if column == plot_consts.STATISTICS_KEY.EXPERIENCE.value:
        return consts.DEFAULT_VALUES.EXPERIENCE.value
    return None


def __get_statistics_info_for_plots(column: plot_consts.STATISTICS_KEY):
    return {
        plot_consts.STATISTICS_INFO_FOR_PLOTS.LABELS.value: __get_labels_for_plots(column),
        plot_consts.STATISTICS_INFO_FOR_PLOTS.TITLE.value: __get_title_for_plots(column)
    }


def __plot_pie_chart(statistics_df: pd.DataFrame, title: str, path: str, column: plot_consts.STATISTICS_KEY,
                     labels: dict, plot_name='distribution_plot',
                     format=consts.EXTENSION.HTML.value, auto_open=False):
    fig = px.pie(statistics_df, values=plot_consts.STATISTICS_FREQ, names=column, title=title,
                 color_discrete_sequence=plot_consts.STATISTICS_COLORS.PIE_CHART.value,
                 hover_data=[plot_consts.STATISTICS_FREQ],
                 labels=labels)
    fig.update_traces(textposition='inside', textinfo='percent')
    save_plot(fig, path, plot_consts.PLOT_TYPES.PIE.value, plot_name, format, auto_open)


def __plot_bar_chart(statistics_df: pd.DataFrame, column: plot_consts.STATISTICS_KEY,
                     title: str, labels: dict,
                     path: str, plot_name='distribution_plot', format=consts.EXTENSION.HTML.value,
                     auto_open=False, x_category_order=plot_consts.PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING.value):
    # x_category_order='total ascending' means: in order of increasing values in Y
    # x_category_order='category ascending' means: in order of increasing values in X
    fig = px.bar(statistics_df, x=column, y=plot_consts.STATISTICS_FREQ, title=title, labels=labels,
                 hover_data=[column, plot_consts.STATISTICS_FREQ])
    fig.update_layout(
        yaxis=dict(
            title_text=plot_consts.STATISTICS_SHOWING_KEY.FREQ.value
        ),
        xaxis=dict(
            title_text=get_readable_key(str(column)),
            # We use type = 'category' because we want to display all values (numbers and strings)
            type='category',
            categoryorder=x_category_order
        ),
        plot_bgcolor=plot_consts.STATISTICS_COLORS.BAR_CHART_BG.value
    )
    fig.update_yaxes(automargin=True)
    save_plot(fig, path, plot_consts.PLOT_TYPES.BAR.value, plot_name, format, auto_open)


def plot_profile_statistics(file: str, column: plot_consts.STATISTICS_KEY, plot_type: plot_consts.PLOT_TYPES,
                            to_union_rare=False, format=consts.EXTENSION.HTML.value, auto_open=False,
                            x_category_order=plot_consts.PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING.value):
    default_value = __get_default_value_for_plots(column)
    statistics_df = __get_statistics_df_from_file(file, column, default_value, to_union_rare)
    path = get_parent_folder(file)
    labels = __get_statistics_info_for_plots(column)
    title = __get_title_for_plots(column)
    if plot_type == plot_consts.PLOT_TYPES.PIE.value:
        __plot_pie_chart(statistics_df, title, path, column, labels, plot_name=str(column), format=format,
                         auto_open=auto_open)
    elif plot_type == plot_consts.PLOT_TYPES.BAR.value:
        __plot_bar_chart(statistics_df, column, title, labels, path, plot_name=str(column), format=format,
                         auto_open=auto_open, x_category_order=x_category_order)
    else:
        log.error(f'Plot type {plot_type} is incorrect!')
        raise ValueError(f'Plot type {plot_type} is incorrect!')