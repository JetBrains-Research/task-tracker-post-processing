# Copyright (c) by anonymous author(s)

import os
import subprocess
from typing import List
from subprocess import check_output

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.consts import TEST_DATA_PATH, CLI_PATH
from src.main.util.consts import RUNNING_TESTS_OUTPUT_DIRECTORY
from src.main.util.file_util import get_parent_folder, remove_directory
from src.main.cli.configs import PREPROCESSING_PARAMS, PREPROCESSING_LEVEL


BASE_FOLDER_NAME = 'preprocessing'
PREPROCESSING_OUTPUT_PREFIX = 'preprocessing_output'
DATA_PATH = os.path.join(TEST_DATA_PATH, 'cli', BASE_FOLDER_NAME)


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.CLI), reason=TEST_LEVEL.CLI.value)
class TestPreprocessingCli:

    @staticmethod
    def __get_args(params: List[str], data_path: str = DATA_PATH) -> List[str]:
        return ['python3', os.path.join(CLI_PATH, 'preprocessing.py'), data_path] + params

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        [],
                        [PREPROCESSING_PARAMS.LEVEL.value, str(PREPROCESSING_LEVEL.min_value())],
                        [PREPROCESSING_PARAMS.LEVEL.value, str(PREPROCESSING_LEVEL.max_value())]
                    ])
    def param_data_preprocessing(request) -> List[str]:
        return request.param

    # Correct cases
    def test_data_preprocessing(self, param_data_preprocessing) -> None:
        output = check_output(self.__get_args(param_data_preprocessing))
        # Delete the new folders
        remove_directory(os.path.join(get_parent_folder(DATA_PATH),
                                      f'{BASE_FOLDER_NAME}_{PREPROCESSING_OUTPUT_PREFIX}'))
        remove_directory(os.path.join(get_parent_folder(DATA_PATH),
                                      f'{BASE_FOLDER_NAME}_{PREPROCESSING_OUTPUT_PREFIX}_{RUNNING_TESTS_OUTPUT_DIRECTORY}'))

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        [PREPROCESSING_PARAMS.LEVEL.value, str(PREPROCESSING_LEVEL.max_value() + 1)],
                        [PREPROCESSING_PARAMS.LEVEL.value, str(PREPROCESSING_LEVEL.min_value() - 1)],
                        [PREPROCESSING_PARAMS.LEVEL.value, 'not_number'],
                    ])
    def param_error_values(request) -> List[str]:
        return request.param

    # Test the error parameters values
    def test_error_values(self, param_error_values) -> None:
        with pytest.raises(subprocess.CalledProcessError):
            output = check_output(self.__get_args(param_error_values))