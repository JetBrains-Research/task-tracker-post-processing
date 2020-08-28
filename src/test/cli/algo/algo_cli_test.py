# Copyright (c) by anonymous author(s)

import os
import subprocess
from typing import List, Union
from subprocess import check_output

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.cli.configs import ALGO_PARAMS, ALGO_LEVEL
from src.main.util.consts import CLI_PATH, TEST_DATA_PATH, TASK
from src.main.solution_space.solution_space_handler import construct_solution_graph
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer


DATA_PATH = os.path.join(TEST_DATA_PATH, 'cli', 'algo', TASK.PIES.value)


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.CLI), reason=TEST_LEVEL.CLI.value)
class TestAlgoCli:

    @staticmethod
    def __get_args(params: List[Union[ALGO_PARAMS, str]], data_path: str = DATA_PATH, to_get_values: bool = True) -> List[str]:
        if to_get_values:
            params = [p.value for p in params]
        return ['python3', os.path.join(CLI_PATH, 'algo.py'), data_path] + \
               [ALGO_PARAMS.TASK.value, TASK.PIES.value] + \
               params


    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        [],
                        [ALGO_PARAMS.CONSTRUCT],
                        [ALGO_PARAMS.CONSTRUCT, ALGO_PARAMS.SERIALIZE],
                        [ALGO_PARAMS.CONSTRUCT, ALGO_PARAMS.SERIALIZE, ALGO_PARAMS.VISUALIZE]
                    ])
    def param_constructing_graph(request) -> List[ALGO_PARAMS]:
        return request.param

    # Correct cases
    def test_constructing_graph(self, param_constructing_graph) -> None:
        output = check_output(self.__get_args(param_constructing_graph))

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        [ALGO_PARAMS.DESERIALIZE, ALGO_PARAMS.CONSTRUCT],
                        # It is an error combination, because a path with the graph does not exist
                        [ALGO_PARAMS.DESERIALIZE]
                    ])
    def param_error_combinations(request) -> List[ALGO_PARAMS]:
        return request.param

    # Test the error parameters combinations
    def test_error_combinations(self, param_error_combinations) -> None:
        with pytest.raises(subprocess.CalledProcessError):
            output = check_output(self.__get_args(param_error_combinations))

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        [],
                        [ALGO_PARAMS.DESERIALIZE],
                        [ALGO_PARAMS.DESERIALIZE, ALGO_PARAMS.SERIALIZE],
                        [ALGO_PARAMS.DESERIALIZE, ALGO_PARAMS.SERIALIZE, ALGO_PARAMS.VISUALIZE]
                    ])
    def param_deserialize_graph(request) -> List[ALGO_PARAMS]:
        return request.param

    def test_deserialize_graph(self, param_deserialize_graph) -> None:
        # Construct the graph and then run the test with it
        graph = construct_solution_graph(DATA_PATH, TASK.PIES)
        path = SolutionSpaceSerializer.serialize(graph)
        output = check_output(self.__get_args(param_deserialize_graph, path))

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        [ALGO_PARAMS.LEVEL.value, str(ALGO_LEVEL.max_value() + 1)],
                        [ALGO_PARAMS.LEVEL.value, str(ALGO_LEVEL.min_value() - 1)],
                        [ALGO_PARAMS.LEVEL.value, 'not_number'],
                        [ALGO_PARAMS.TASK.value, 'incorrect_task']
                    ])
    def param_error_values(request) -> List[str]:
        return request.param

    # Test the error parameters values
    def test_error_values(self, param_error_values) -> None:
        with pytest.raises(subprocess.CalledProcessError):
            output = check_output(self.__get_args(param_error_values, to_get_values=False))
