# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os

from src.test.test_util import LoggedTest
from src.main.util.consts import TEST_DATA_PATH
from src.main.plots.splitting_plots import create_comparative_splitting_plot

DATA = os.path.join(TEST_DATA_PATH, 'plots/data.csv')


# Just to check no errors are raised during plot creation
class TestSplittingPlots(LoggedTest):

    def test_plot_creation(self) -> None:
        create_comparative_splitting_plot(DATA, to_show=True)
