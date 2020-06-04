# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from itertools import groupby
from typing import Dict, List
from collections import defaultdict

import pandas as pd
import plotly.graph_objects as go

from src.main.util import consts
from src.main.canonicalization.consts import TREE_TYPE
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.plots.util.plots_common import get_readable_key, get_labels_for_freq_plots
from src.main.plots.util.plotly_util import save_plot, get_freq_bar_chart, update_layout, plot_and_save_freq_chart
from src.main.statistics_gathering.solution_graph_statistics import get_node_numbers_solution_graph_statistics, \
    get_node_numbers_freq_statistics_for_each_vertex
from src.main.plots.util.consts import STATISTICS_KEY, PLOTTY_CATEGORY_ORDER, STATISTICS_FREQ, PLOT_TYPE, \
    DEFAULT_PATH_FOR_PLOTS


log = logging.getLogger(consts.LOGGER_NAME)


def plot_node_numbers_statistics(solution_graph: SolutionGraph, path: str = DEFAULT_PATH_FOR_PLOTS,
                                 format: consts.EXTENSION = consts.EXTENSION.HTML, auto_open: bool = False,
                                 x_category_order: PLOTTY_CATEGORY_ORDER = PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING) -> None:
    canon_trees_statistics, anon_trees_statistics = get_node_numbers_solution_graph_statistics(solution_graph)
    log.info(f'Nodes number statistics for canon and anon trees has collected')
    labels = get_labels_for_freq_plots(STATISTICS_KEY.NODES_NUMBER)
    column = STATISTICS_KEY.NODES_NUMBER
    canon_trees_statistics_df = pd.DataFrame(canon_trees_statistics.items(), columns=[column.value, STATISTICS_FREQ])
    log.info(f'Start plotting canon trees statistics')
    plot_and_save_freq_chart(canon_trees_statistics_df, title='Vertices number for canon trees', path=path,
                             column=column, labels=labels, plot_name='vertices_number_for_canon_trees', format=format,
                             auto_open=auto_open, x_category_order=x_category_order)
    log.info(f'Finish plotting canon trees statistics')
    anon_trees_statistics_df = pd.DataFrame(anon_trees_statistics.items(), columns=[column.value, STATISTICS_FREQ])
    log.info(f'Start plotting anon trees statistics')
    plot_and_save_freq_chart(anon_trees_statistics_df, title='Vertices number for anon trees', path=path, column=column,
                             labels=labels, plot_name='vertices_number_for_anon_trees', format=format,
                             auto_open=auto_open, x_category_order=x_category_order)
    log.info(f'Finish plotting anon trees statistics')


def __add_canon_nodes_numbers(fig: go.Figure, canon_nodes_number: int,
                              anon_nodes_number_freq: Dict[int, int]) -> go.Figure:
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=[canon_nodes_number],
            y=[anon_nodes_number_freq.get(canon_nodes_number, 1) / 2],
            marker=dict(
                color='White',
                size=20,
                line=dict(width=1, color='DarkSlateGrey')
            ),
            showlegend=False,
            marker_symbol='x',
            hoverinfo='skip'
        )
    )
    return fig


def __plot_node_numbers_freq_for_vertex(vertex_id: int, labels: Dict[str, str], anon_nodes_numbers: List[int],
                                        canon_nodes_number: int, path: str, format: consts.EXTENSION, auto_open: bool,
                                        column: STATISTICS_KEY = STATISTICS_KEY.NODES_NUMBER) -> None:
    title = __get_title_for_vertex_plot(vertex_id)
    freq_dict = defaultdict(int)
    for key, group in groupby(anon_nodes_numbers):
        freq_dict[key] = len(list(group))
    statistics_df = pd.DataFrame(freq_dict.items(), columns=[column.value, STATISTICS_FREQ])
    fig = get_freq_bar_chart(statistics_df, title, column, labels,
                             x_category_order=PLOTTY_CATEGORY_ORDER.TRACE,
                             to_update_layout=False)
    __add_canon_nodes_numbers(fig, canon_nodes_number, freq_dict)
    # Todo: fix x_category_order, because now order is not always ascending
    fig = update_layout(fig, column, PLOTTY_CATEGORY_ORDER.TRACE)
    save_plot(fig, path, PLOT_TYPE.BAR, f'vertex_{vertex_id}', format, auto_open)


def __get_title_for_vertex_plot(vertex_id_: int, column: STATISTICS_KEY = STATISTICS_KEY.NODES_NUMBER) -> str:
    return f'{get_readable_key(column.value)} distribution for anon trees for vertex with id {vertex_id_}'


def plot_node_numbers_freq_for_each_vertex(solution_graph: SolutionGraph, path: str = DEFAULT_PATH_FOR_PLOTS,
                                           format: consts.EXTENSION = consts.EXTENSION.PNG, auto_open: bool = False) -> None:
    statistics = get_node_numbers_freq_statistics_for_each_vertex(solution_graph)
    log.info(f'Nodes number statistics for each vertex for canon and anon trees has collected')
    labels = get_labels_for_freq_plots(STATISTICS_KEY.NODES_NUMBER)
    for vertex_id in statistics.keys():
        log.info(f'Start plotting nodes number statistics for vertex {vertex_id}')
        __plot_node_numbers_freq_for_vertex(vertex_id, labels, statistics[vertex_id][TREE_TYPE.ANON],
                                            statistics[vertex_id][TREE_TYPE.CANON], path, format, auto_open)
        log.info(f'Finish plotting nodes number statistics for vertex {vertex_id}')
