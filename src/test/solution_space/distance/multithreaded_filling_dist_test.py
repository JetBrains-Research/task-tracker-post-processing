# Copyright (c) by anonymous author(s)

import logging
from datetime import datetime

import pytest

from src.main.util.consts import TASK, LOGGER_NAME
from src.test.test_config import to_skip, TEST_LEVEL
from src.test.solution_space.util import get_solution_graph

log = logging.getLogger(LOGGER_NAME)

expected_dist_matrix = [[0,  22, 15, 20, 1,  13, 21, 56, 61],
                        [22, 0,  39, 39, 39, 42, 49, 83, 88],
                        [15, 39, 0,  5,  34, 40, 41, 64, 69],
                        [20, 39, 5,  0,  39, 45, 46, 69, 68],
                        [1,  39, 34, 39, 0,  8,  16, 51, 56],
                        [13, 42, 40, 45, 8,  0,  8,  43, 48],
                        [21, 49, 41, 46, 16, 8,  0,  35, 40],
                        [56, 83, 64, 69, 51, 43, 35, 0,  5 ],
                        [61, 88, 69, 68, 56, 48, 40, 5,  0 ]]


@pytest.mark.skip(reason='We don\'t use dist in solution graph anymore')
class TestMultithreadedFillingDist:

    @pytest.mark.skip(reason='Filling expected matrix takes a lot of time, so we compare it with pre-filled one. '
                             'This test is only needed to check pre-filled one, so we can skip it.')
    def test_expected_matrix_filled_right(self):
        # Time with storing dist: 0:07:57
        start_time = datetime.now()
        sg_with_dist = get_solution_graph(TASK.PIES, to_plot_graph=False)
        end_time = datetime.now()
        sg_with_dist_time = end_time - start_time
        dist_matrix = sg_with_dist._dist._IDistanceMatrix__get_dist_matrix()
        log.info(f'expected_dist_matrix: {dist_matrix}, time: {sg_with_dist_time}')
        assert dist_matrix == expected_dist_matrix

    def test_filling_dist(self):
        # Time with multithreading: 0:04:50
        start_time = datetime.now()
        sg_without_dist = get_solution_graph(TASK.PIES, to_plot_graph=False)
        sg_without_dist.to_store_dist = True
        end_time = datetime.now()
        sg_without_dist_time = end_time - start_time

        actual_dist_matrix = sg_without_dist._dist._IDistanceMatrix__get_dist_matrix()

        log.info(f'Time without storing dist: {sg_without_dist_time}')
        assert actual_dist_matrix == expected_dist_matrix
