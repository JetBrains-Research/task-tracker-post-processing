# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import sys
import logging
import argparse
from datetime import datetime
from enum import Enum

import pandas as pd

from src.main.util.configs import ACTIONS_TYPE, PREPROCESSING_LEVEL

sys.path.append('.')
from src.main.util import consts
from src.main.util.file_util import add_slash, get_all_file_system_items, language_item_condition
from src.main.util.log_util import configure_logger
from src.main.solution_space.hint import HintHandler
from src.main.splitting.tasks_tests_handler import run_tests
from src.main.solution_space.consts import TEST_SYSTEM_GRAPH
from src.main.solution_space.data_classes import User, CodeInfo
from src.main.preprocessing.preprocessing import preprocess_data
from src.main.plots.tasks_statistics_plots import plot_tasks_statistics
from src.main.splitting.splitting import split_tasks_into_separate_files
from src.main.preprocessing.int_experience_adding import add_int_experience
from src.main.plots.profile_statistics_plots import plot_profile_statistics
from src.main.util.consts import PATH_CMD_ARG, TASK, INT_EXPERIENCE, TEST_RESULT, FILE_SYSTEM_ITEM
from src.main.solution_space.path_finder_test_system import TestSystem, TEST_INPUT
from src.main.solution_space.solution_space_handler import construct_solution_graph
from src.main.statistics_gathering.statistics_gathering import get_profile_statistics
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer
from src.main.solution_space.solution_space_visualizer import SolutionSpaceVisualizer
from src.main.plots.util.consts import PLOTTY_CATEGORY_ORDER, STATISTICS_KEY, PLOT_TYPE
from src.main.preprocessing.intermediate_diffs_removing import remove_intermediate_diffs
from src.main.preprocessing.inefficient_statements_removing import remove_inefficient_statements
from src.main.plots.solution_graph_statistics_plots import plot_node_numbers_statistics, \
    plot_node_numbers_freq_for_each_vertex

pd.set_option('display.max_rows', 250)
pd.set_option('display.max_columns', 100)

log = logging.getLogger(consts.LOGGER_NAME)


parser = argparse.ArgumentParser(description='Coding Assistant project.')


def __configure_args() -> None:
    parser.add_argument('path', type=str, nargs=1, help='data path')
    parser.add_argument('action', type=str, nargs=1, choices=ACTIONS_TYPE.values(),
                        help='current action')
    parser.add_argument('--level', nargs='?', const=-1, default=-1, help='preprocessing level')


def __split_into_tasks(path: str) -> str:
    split_tasks_into_separate_files(path)
    pass
    return path


def __data_preprocessing(path: str, preprocessing_level: PREPROCESSING_LEVEL) -> None:
    preprocessing_functions = [preprocess_data, run_tests, split_tasks_into_separate_files, remove_intermediate_diffs,
                               remove_inefficient_statements, add_int_experience]

    start_function_index = 0
    end_function_index = preprocessing_level.value \
        if preprocessing_level != PREPROCESSING_LEVEL.ALL else PREPROCESSING_LEVEL.max_value()

    paths = [path]
    for function_index in range(start_function_index, end_function_index + 1):
        log.info(f'Current operation is {preprocessing_functions[function_index]}')
        new_paths = []
        for path in paths:
            path = preprocessing_functions[function_index](path)
            if function_index == PREPROCESSING_LEVEL.SPLIT:
                # Get all sub folders
                new_paths += get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
            else:
                new_paths.append(path)
        paths = new_paths


def __get_preprocessing_level(level: int) -> PREPROCESSING_LEVEL:
    try:
        return PREPROCESSING_LEVEL(level)
    except ValueError:
        message = f'Preprosessing level have to be an integer number from {PREPROCESSING_LEVEL.min_value()} ' \
                  f'to {PREPROCESSING_LEVEL.max_value()}'
        log.error(message)
        raise ValueError(message)


def main() -> None:
    configure_logger(to_delete_previous_logs=True)
    __configure_args()
    args = parser.parse_args()
    path = add_slash(args.path[0])
    action = ACTIONS_TYPE(args.action[0])

    if action == ACTIONS_TYPE.PREPROCESSING:
        level = __get_preprocessing_level(args.level)
        __data_preprocessing(path, level)
    elif action == ACTIONS_TYPE.STATISTICS:
        pass
    elif action == ACTIONS_TYPE.ALGO:
        pass


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
    Graph constructing
    """
    # task = TASK.PIES
    # graph = construct_solution_graph(path, task)
    # print('Graph was constructed')

    """
    Nodes number statistics
    """
    # plot_node_numbers_statistics(graph)
    # print('Created plot with node numbers statistics')
    # plot_node_numbers_freq_for_each_vertex(graph)
    # print('Created plots with node numbers freq for each vertex')
    """
    Graph serialization
    """
    # path = SolutionSpaceSerializer.serialize(graph, serialized_file_prefix='serialized_graph_with_nodes_number')
    # print(f'Serialized path: {path}')
    # new_graph = SolutionSpaceSerializer.deserialize(path)
    # print(str(graph) == str(new_graph))

    # test_system_graph = SolutionSpaceSerializer.deserialize(TEST_SYSTEM_GRAPH)
    # print('done')
    # print(str(graph) == str(test_system_graph))

    """
    Graph visualization
    """
    # gv = SolutionSpaceVisualizer(graph)
    # graph_visualization_path = gv.visualize_graph(name_prefix=f'{task.value}_full')
    # print(graph_visualization_path)

    """
    Getting hint
    """
    # source = 'a = int(input())\nb = int(input())\nn = int(input())'
    # code_info = CodeInfo(User())
    # hint_handler = HintHandler(graph, PathFinderV2, MeasuredVertexV1)
    # hint = hint_handler.get_hint(source, code_info)
    # print(hint.recommended_code)

    """
    Running test system
    """
    # It's possible not to include TEST_INPUT.RATE in dict, in this case it will be found by
    # running tests on TEST_INPUT.SOURCE_CODE.
    # However, to speed up the process, one may include TEST_INPUT.RATE.
    # ages = [12, 15, 18]
    # experiences = [INT_EXPERIENCE.LESS_THAN_HALF_YEAR, INT_EXPERIENCE.FROM_ONE_TO_TWO_YEARS,
    #                INT_EXPERIENCE.MORE_THAN_SIX]
    # test_fragments = TestSystem.generate_all_test_fragments(ages, experiences, TestSystem.get_fragments_for_task(task))
    # ts = TestSystem(test_fragments, task=task, add_same_docs=False, graph=graph)


if __name__ == '__main__':
    main()
