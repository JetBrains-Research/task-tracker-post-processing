# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import sys
import logging

import pandas as pd

sys.path.append('.')
sys.path.append('../..')
from src.main.util import consts
from src.main.util.log_util import configure_logger
from src.main.plots.tasks_statistics_plots import plot_tasks_statistics
from src.main.plots.profile_statistics_plots import plot_profile_statistics
from src.main.statistics_gathering.statistics_gathering import get_profile_statistics
from src.main.plots.util.consts import PLOTTY_CATEGORY_ORDER, STATISTICS_KEY, CHART_TYPE
from src.main.plots.solution_graph_statistics_plots import plot_node_numbers_statistics, \
    plot_node_numbers_freq_for_each_vertex

pd.set_option('display.max_rows', 250)
pd.set_option('display.max_columns', 100)

log = logging.getLogger(consts.LOGGER_NAME)


def main() -> None:
    configure_logger(to_delete_previous_logs=True)
    """
    Plot profile statistics
    Note: Run before 'split_tasks_into_separate_files' 
    """
    # statistics_path = get_profile_statistics(path)
    # # Plot age statistics
    # age_path = os.path.join(statistics_path, 'age.pickle')
    # plot_profile_statistics(age_path, STATISTICS_KEY.AGE, PLOT_TYPE.BAR, auto_open=True,
    #                         x_category_order=PLOTTY_CATEGORY_ORDER.CATEGORY_ASCENDING)
    # plot_profile_statistics(age_path, STATISTICS_KEY.AGE, PLOT_TYPE.PIE, auto_open=True,
    #                         to_union_rare=True)
    # # Plot experience statistics
    # experience_path = os.path.join(statistics_path, 'programExperience.pickle')
    # plot_profile_statistics(experience_path, STATISTICS_KEY.EXPERIENCE, PLOT_TYPE.BAR, auto_open=True)
    # plot_profile_statistics(experience_path, STATISTICS_KEY.EXPERIENCE, PLOT_TYPE.PIE, auto_open=True,
    #                         to_union_rare=True)
    """
    Plot tasks statistics
    Note: Run after 'split_tasks_into_separate_files'
    """
    # plot_tasks_statistics(path)
    """
    Nodes number statistics
    """
    # plot_node_numbers_statistics(graph)
    # print('Created plot with node numbers statistics')
    # plot_node_numbers_freq_for_each_vertex(graph)
    # print('Created plots with node numbers freq for each vertex')


if __name__ == '__main__':
    main()
