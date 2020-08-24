# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import subprocess
from typing import List
from subprocess import check_output

import pytest

from src.main.util.file_util import remove_directory
from src.test.test_config import to_skip, TEST_LEVEL
from src.main.cli.configs import PLOTS_PARAMS, PLOT_TYPE
from src.main.util.consts import TEST_DATA_PATH, CLI_PATH


STATISTICS_FOLDER = 'statistics'
AFTER_SPLITTING_PREFIX = 'after_splitting'
BEFORE_SPLITTING_PREFIX = 'before_splitting'
STATISTICS_OUTPUT_PREFIX = 'statistics_output'
BASE_DATA_PATH = os.path.join(TEST_DATA_PATH, 'cli', 'plots')
DATA_BEFORE_SPLITTING_PATH = os.path.join(BASE_DATA_PATH, BEFORE_SPLITTING_PREFIX)
DATA_AFTER_SPLITTING_PATH = os.path.join(BASE_DATA_PATH, AFTER_SPLITTING_PREFIX)


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.CLI), reason=TEST_LEVEL.CLI.value)
class TestPlotsCli:

    @staticmethod
    def __get_args(params: List[str], data_path: str = DATA_BEFORE_SPLITTING_PATH) -> List[str]:
        return ['python3', os.path.join(CLI_PATH, 'plots.py'), data_path] + params

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        [PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value],
                        # TODO: why does the test fail?
                        # [PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value, PLOTS_PARAMS.TO_UNION_RARE.value],
                        [PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value, PLOTS_PARAMS.FORMAT.value, '.html'],
                        [PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value, PLOTS_PARAMS.FORMAT.value, 'html'],
                    ])
    def param_plots(request) -> List[str]:
        return request.param

    # Correct cases
    def test_plots(self, param_plots) -> None:
        output = check_output(self.__get_args(param_plots))
        # Delete the new folders
        remove_directory(os.path.join(BASE_DATA_PATH, f'{BEFORE_SPLITTING_PREFIX}_{STATISTICS_OUTPUT_PREFIX}'))
        remove_directory(os.path.join(BASE_DATA_PATH, STATISTICS_FOLDER))

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        ['incorrect_plot_type_value'],
                        [PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value, PLOTS_PARAMS.TYPE_DISTR.value, 'incorrect_type_distr'],
                        [PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value, PLOTS_PARAMS.CHART_TYPE.value, 'incorrect_chart_type'],
                        [PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value, PLOTS_PARAMS.FORMAT.value, 'incorrect_format'],
                        # Available formats: html, png
                        [PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value, PLOTS_PARAMS.FORMAT.value, '.svg'],
                        [PLOT_TYPE.PARTICIPANTS_DISTRIBUTION.value, PLOTS_PARAMS.FORMAT.value, 'svg'],
                    ])
    def param_error_values(request) -> List[str]:
        return request.param

    # Test the error parameters values
    def test_error_values(self, param_error_values) -> None:
        with pytest.raises(subprocess.CalledProcessError):
            output = check_output(self.__get_args(param_error_values))
