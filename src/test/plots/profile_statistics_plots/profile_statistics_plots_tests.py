# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os

from src.test.test_util import LoggedTest
from src.test.plots.util import TO_OPEN_PLOTS
from src.main.util.consts import TEST_DATA_PATH
from src.main.plots.util.consts import STATISTICS_KEY, PLOT_TYPE
from src.main.plots.profile_statistics_plots import plot_profile_statistics
from src.main.statistics_gathering.statistics_gathering import get_profile_statistics

DATA_PATH = os.path.join(TEST_DATA_PATH, 'plots/profile_statistics_plots/')
STATISTICS_PATH = os.path.join(TEST_DATA_PATH, 'plots/data.csv')


# Just to check no errors are raised during plot creation
class TestProfileStatisticsPlots(LoggedTest):

    def test_plot_creation(self) -> None:
        result_path = get_profile_statistics(DATA_PATH)
        age_statistics = [os.path.join(result_path, 'age.pickle'), STATISTICS_KEY.AGE]
        experience_statistics = [os.path.join(result_path, 'programExperience.pickle'), STATISTICS_KEY.EXPERIENCE]
        for statistics, column in [age_statistics, experience_statistics]:
            for type in PLOT_TYPE:
                plot_profile_statistics(statistics, column, type, auto_open=TO_OPEN_PLOTS)

