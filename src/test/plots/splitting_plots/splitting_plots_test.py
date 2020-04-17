# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import pytest

from src.test.plots.util import TO_OPEN_PLOTS
from src.test.util import does_skip, TEST_LEVEL
from src.main.util.consts import TEST_DATA_PATH
from src.main.plots.splitting_plots import create_comparative_splitting_plot

DATA = os.path.join(TEST_DATA_PATH, 'plots/data.csv')


# Just to check no errors are raised during plot creation
@pytest.mark.skipif(does_skip(current_module_level=TEST_LEVEL.PLOTS), reason=TEST_LEVEL.PLOTS.value)
class TestSplittingPlots:

    def test_plot_creation(self) -> None:
        create_comparative_splitting_plot(DATA, to_show=TO_OPEN_PLOTS)
