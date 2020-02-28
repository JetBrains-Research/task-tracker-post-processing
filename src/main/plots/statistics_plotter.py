import os
import plotly
import logging
import pandas as pd
import plotly.express as px


from src.main.util import consts
from src.main.plots import consts as stat_const
from src.main.util.file_util import get_parent_folder, get_content_from_file, change_extension_to, create_directory, deserialize_data_from_file


log = logging.getLogger(consts.LOGGER_NAME)


# Get key, which will be shown on a plot
def __get_readable_key(key: str, default_value=None):
    # It was an incorrect file
    if key == '-1':
        return stat_const.STATISTICS_SHOWING_KEY.INCORRECT.value
    # It was not indicated
    if key == str(default_value):
        return stat_const.STATISTICS_SHOWING_KEY.NOT_INDICATED.value
    return key.replace('_', ' ').capitalize()


def __read_statistics_file(path: str, default_value: consts.DEFAULT_VALUES):
    statistics_dict = deserialize_data_from_file(path)
    readable_statistics_dict = {}
    for key in statistics_dict.keys():
        readable_statistics_dict[__get_readable_key(key, default_value)] = statistics_dict[key]
    return readable_statistics_dict


def __filter_rare_values(statistics_df: pd.DataFrame):
    return statistics_df[stat_const.STATISTIC_FREQ] <= stat_const.STATISTICS_RARE_VALUE_THRESHOLD


def __get_statistics_from_file(path: str, column: stat_const.STATISTIC_KEY, default_value: consts.DEFAULT_VALUES,
                               to_union_rare=False):
    statistics_dict = __read_statistics_file(path, default_value)
    statistics_df = pd.DataFrame(statistics_dict.items(), columns=[column, stat_const.STATISTIC_FREQ])
    # If we want to union rare values
    if to_union_rare:
        statistics_df.loc[__filter_rare_values(statistics_df), column] = stat_const.STATISTICS_SHOWING_KEY.OTHERS.value
    return statistics_df


def __create_directory_for_plots(path: str, folder: stat_const.PLOT_TYPES, file_name: str):
    path = os.path.join(path, str(folder))
    create_directory(path)
    return os.path.join(path, file_name)


def __plot_pie_chart(statistics_df: pd.DataFrame, title: str, path: str, column: stat_const.STATISTIC_KEY,
                     labels: dict, plot_name='result_plot',
                     format=stat_const.OUTPUT_FORMAT.HTML.value, auto_open=False):
    fig = px.pie(statistics_df, values=stat_const.STATISTIC_FREQ, names=column, title=title,
                 color_discrete_sequence=stat_const.STATISTICS_COLORS.PIE_CHART.value,
                 hover_data=[stat_const.STATISTIC_FREQ],
                 labels=labels)
    fig.update_traces(textposition='inside', textinfo='percent')
    __save_plot(fig, path, stat_const.PLOT_TYPES.PIE.value, plot_name, format, auto_open)


def __save_plot(fig, path: str, plot_type: stat_const.PLOT_TYPES,
                plot_name='result_plot', format=stat_const.OUTPUT_FORMAT.HTML.value, auto_open=False):
    file_name = __create_directory_for_plots(path, plot_type, change_extension_to(plot_name, format))
    plotly.offline.plot(fig, filename=file_name, auto_open=auto_open)


def __plot_bar_chart(statistics_df: pd.DataFrame, column: stat_const.STATISTIC_KEY,
                     title: str, labels: dict,
                     path: str, plot_name='result_plot', format=stat_const.OUTPUT_FORMAT.HTML.value,
                     auto_open=False, x_category_order=stat_const.PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING.value):
    # x_category_order='total ascending' means: in order of increasing values in Y
    # x_category_order='category ascending' means: in order of increasing values in X
    fig = px.bar(statistics_df, x=column, y=stat_const.STATISTIC_FREQ, title=title, labels=labels,
                 hover_data=[column, stat_const.STATISTIC_FREQ])
    fig.update_layout(
        yaxis=dict(
            title_text=stat_const.STATISTICS_SHOWING_KEY.FREQ.value
        ),
        xaxis=dict(
            title_text=__get_readable_key(str(column)),
            # We use type = 'category' because we want to display all values (numbers and strings)
            type='category',
            categoryorder=x_category_order
        ),
        plot_bgcolor=stat_const.STATISTICS_COLORS.BAR_CHART_BG.value
    )
    fig.update_yaxes(automargin=True)
    __save_plot(fig, path, stat_const.PLOT_TYPES.BAR.value, plot_name, format, auto_open)


def __get_labels_for_plots(column: stat_const.STATISTIC_KEY):
    return {
        stat_const.STATISTIC_FREQ: stat_const.STATISTICS_SHOWING_KEY.FREQ.value,
        column: __get_readable_key(str(column))
    }


def __get_title_for_plots(column: stat_const.STATISTIC_KEY):
    return __get_readable_key(str(column)) + ' distribution'


def __get_default_value_for_plots(column: stat_const.STATISTIC_KEY):
    if column == stat_const.STATISTIC_KEY.AGE.value:
        return consts.DEFAULT_VALUES.AGE.value
    if column == stat_const.STATISTIC_KEY.EXPERIENCE.value:
        return consts.DEFAULT_VALUES.EXPERIENCE.value
    return None


def __get_statistics_info_for_plots(column: stat_const.STATISTIC_KEY):
    return {
        stat_const.STATISTICS_INFO_FOR_PLOTS.LABELS.value: __get_labels_for_plots(column),
        stat_const.STATISTICS_INFO_FOR_PLOTS.TITLE.value: __get_title_for_plots(column)
    }


def plot_statistics(file: str, column: stat_const.STATISTIC_KEY, plot_type: stat_const.PLOT_TYPES,
                    to_union_rare=False, format=stat_const.OUTPUT_FORMAT.HTML.value, auto_open=False,
                    x_category_order=stat_const.PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING.value):
    default_value = __get_default_value_for_plots(column)
    statistics_df = __get_statistics_from_file(file, column, default_value, to_union_rare)
    path = get_parent_folder(file)
    labels = __get_statistics_info_for_plots(column)
    title = __get_title_for_plots(column)
    if plot_type == stat_const.PLOT_TYPES.PIE.value:
        __plot_pie_chart(statistics_df, title, path, column, labels, plot_name=str(column), format=format,
                         auto_open=auto_open)
    elif plot_type == stat_const.PLOT_TYPES.BAR.value:
        __plot_bar_chart(statistics_df, column, title, labels, path, plot_name=str(column), format=format,
                         auto_open=auto_open, x_category_order=x_category_order)
    else:
        log.error(f'Plot type {plot_type} is incorrect!')
        raise ValueError(f'Plot type {plot_type} is incorrect!')