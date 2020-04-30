# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Dict

import pandas as pd
import plotly.express as px

from src.main.util import consts
from src.main.plots.util.plotly_util import save_plot
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.plots.util.plots_common import get_readable_key, get_labels_for_plots
from src.main.statistics_gathering.solution_graph_statistics import get_general_solution_graph_statistics
from src.main.plots.util.consts import STATISTICS_KEY, PLOTTY_CATEGORY_ORDER, STATISTICS_FREQ, STATISTICS_SHOWING_KEY, \
    STATISTICS_COLORS, PLOT_TYPE, DEFAULT_PATH_FOR_PLOTS


def __plot_general_statistics(statistics_dict: Dict[int, int], title: str, path: str, labels: Dict[str, str],
                              plot_name: str = 'general_statistics_plot',
                              column: STATISTICS_KEY = STATISTICS_KEY.VERTICES_NUMBER,
                              format: consts.EXTENSION = consts.EXTENSION.HTML, auto_open: bool = False,
                              x_category_order: PLOTTY_CATEGORY_ORDER = PLOTTY_CATEGORY_ORDER.CATEGORY_ASCENDING) -> None:
    statistics_df = pd.DataFrame(statistics_dict.items(), columns=[column.value, STATISTICS_FREQ])
    # x_category_order='total ascending' means: in order of increasing values in Y
    # x_category_order='category ascending' means: in order of increasing values in X
    fig = px.bar(statistics_df, x=column.value, y=STATISTICS_FREQ, title=title, labels=labels,
                 hover_data=[column.value, STATISTICS_FREQ])
    fig.update_layout(
        yaxis=dict(
            title_text=STATISTICS_SHOWING_KEY.FREQ.value
        ),
        xaxis=dict(
            title_text=get_readable_key(column.value),
            categoryorder=x_category_order.value
        ),
        plot_bgcolor=STATISTICS_COLORS.BAR_CHART_BG.value
    )
    fig.update_yaxes(automargin=True)
    save_plot(fig, path, PLOT_TYPE.BAR, plot_name, format, auto_open)


def plot_general_statistics(solution_graph: SolutionGraph, path: str = DEFAULT_PATH_FOR_PLOTS,
                            format: consts.EXTENSION = consts.EXTENSION.HTML, auto_open: bool = False,
                            x_category_order: PLOTTY_CATEGORY_ORDER = PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING) -> None:
    labels = get_labels_for_plots(STATISTICS_KEY.VERTICES_NUMBER)
    canon_trees_statistics, anon_trees_statistics = get_general_solution_graph_statistics(solution_graph)
    __plot_general_statistics(canon_trees_statistics, title='Vertices number for canon trees', path=path,
                              plot_name='vertices_number_for_canon_trees', format=format, auto_open=auto_open,
                              x_category_order=x_category_order, labels=labels)
    __plot_general_statistics(anon_trees_statistics, title='Vertices number for anon trees', path=path,
                              plot_name='vertices_number_for_anon_trees', format=format, auto_open=auto_open,
                              x_category_order=x_category_order, labels=labels)
