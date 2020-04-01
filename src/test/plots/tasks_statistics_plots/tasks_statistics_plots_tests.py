# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os

from src.test.test_util import LoggedTest
from src.main.util.consts import TEST_DATA_PATH
from src.main.plots.tasks_statistics_plots import plot_tasks_statistics

PATH = os.path.join(TEST_DATA_PATH, 'plots/tasks_statistics_plots')


# Just to check no errors are raised during plot creation
class TestTasksStatisticsPlots(LoggedTest):

    def test_plot_creation(self) -> None:
        plot_tasks_statistics(PATH, auto_open=True)