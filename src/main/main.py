# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import sys
import logging
import argparse
from datetime import datetime
from typing import Union, Type

import pandas as pd

sys.path.append('.')
sys.path.append('../..')
from src.main.util import consts
from src.main.solution_space.hint import HintHandler
from src.main.splitting.tasks_tests_handler import run_tests
from src.main.solution_space.consts import TEST_SYSTEM_GRAPH
from src.main.solution_space.data_classes import User, CodeInfo
from src.main.preprocessing.preprocessing import preprocess_data
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.plots.tasks_statistics_plots import plot_tasks_statistics
from src.main.splitting.splitting import split_tasks_into_separate_files
from src.main.util.log_util import configure_logger, log_and_raise_error
from src.main.preprocessing.int_experience_adding import add_int_experience
from src.main.plots.profile_statistics_plots import plot_profile_statistics
from src.main.solution_space.path_finder.path_finver_v_4 import PathFinderV4
from src.main.solution_space.path_finder_test_system import TestSystem, TEST_INPUT
from src.main.solution_space.measured_tree.measured_tree_v_3 import MeasuredTreeV3
from src.main.solution_space.solution_space_handler import construct_solution_graph
from src.main.statistics_gathering.statistics_gathering import get_profile_statistics
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer
from src.main.solution_space.solution_space_visualizer import SolutionSpaceVisualizer
from src.main.plots.util.consts import PLOTTY_CATEGORY_ORDER, STATISTICS_KEY, PLOT_TYPE
from src.main.preprocessing.intermediate_diffs_removing import remove_intermediate_diffs
from src.main.preprocessing.inefficient_statements_removing import remove_inefficient_statements
from src.main.util.file_util import add_slash, get_all_file_system_items, language_item_condition
from src.main.util.consts import PATH_CMD_ARG, TASK, INT_EXPERIENCE, TEST_RESULT, FILE_SYSTEM_ITEM
from src.main.util.configs import ACTIONS_TYPE, PREPROCESSING_LEVEL, ALGO_LEVEL, DEFAULT_LEVEL_VALUE
from src.main.plots.solution_graph_statistics_plots import plot_node_numbers_statistics, \
    plot_node_numbers_freq_for_each_vertex

pd.set_option('display.max_rows', 250)
pd.set_option('display.max_columns', 100)

log = logging.getLogger(consts.LOGGER_NAME)

parser = argparse.ArgumentParser(description='Coding Assistant project.')


def __get_level_arg_description() -> str:
    # Todo: add statistics level description
    return f'use level param to set level for the action.\n\nAvailable levels for PREPROCESSING:\n' \
           f'{PREPROCESSING_LEVEL.description()}\n' \
           f'Available levels for ALGO:\n' \
           f'{ALGO_LEVEL.description()}'


def __configure_args() -> None:
    parser.add_argument('path', type=str, nargs=1, help='data path')
    parser.add_argument('action', type=str, nargs=1, choices=ACTIONS_TYPE.values(),
                        help='current action')

    parser.add_argument('--level', nargs='?', const=DEFAULT_LEVEL_VALUE, default=DEFAULT_LEVEL_VALUE,
                        help=__get_level_arg_description())
    # Algo args
    parser.add_argument('--construct', nargs='?', const=True, default=True,
                        help='to construct graph. It the argument is False, graph will be deserialized')
    parser.add_argument('--serialize', nargs='?', const=False, default=False, help='to serialize graph')
    parser.add_argument('--viz', nargs='?', const=True, default=True, help='to visualize graph')
    parser.add_argument('--task', nargs='?', const=TASK.PIES.value, default=TASK.PIES.value, help='task for the algo')


def __data_preprocessing(path: str, preprocessing_level: PREPROCESSING_LEVEL) -> None:
    preprocessing_functions = [preprocess_data, run_tests, split_tasks_into_separate_files, remove_intermediate_diffs,
                               remove_inefficient_statements, add_int_experience]
    paths = [path]
    for function_index in range(0,  preprocessing_level.value + 1):
        log.info(f'Current operation is {preprocessing_functions[function_index]}')
        new_paths = []
        for path in paths:
            path = preprocessing_functions[function_index](path)
            if function_index == PREPROCESSING_LEVEL.TESTS_RESULTS.value:
                # Get all sub folders
                new_paths += get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
            else:
                new_paths.append(path)
        paths = list(new_paths)

    str_paths = '\n'.join(paths)
    log.info(f'Folders with data: {str_paths}')
    print(f'Folders with data: {str_paths}')


def __get_task(task: str) -> TASK:
    try:
        return TASK(task)
    except ValueError:
        message = f'Task value has to be one from the values: {TASK.tasks_values()}'
        log.error(message)
        raise ValueError(message)


def __construct_graph(path: str, task: TASK = TASK.PIES, to_construct: bool = True,
               to_serialize: bool = True, to_visualize: bool = True) -> SolutionGraph:
    if to_construct:
        graph = construct_solution_graph(path, task)
        log.info('Graph was constructed')
    else:
        graph = SolutionSpaceSerializer.deserialize(path)
        log.info('Graph was deserialized')

    if to_serialize:
        path = SolutionSpaceSerializer.serialize(graph)
        log.info(f'Serialized graph path: {path}')
        print(f'Serialized graph path: {path}')

    if to_visualize:
        gv = SolutionSpaceVisualizer(graph)
        graph_visualization_path = gv.visualize_graph(name_prefix=f'{task.value}')
        log.info(f'Graph visualization path: {graph_visualization_path}')

    return graph


def __run_algo(path: str, algo_level: ALGO_LEVEL, task: TASK = TASK.PIES, to_construct: bool = True,
               to_serialize: bool = True, to_visualize: bool = True) -> None:
    graph = __construct_graph(path, task, to_construct, to_serialize, to_visualize)

    if algo_level == ALGO_LEVEL.CONSTRUCT:
        return

    if algo_level == ALGO_LEVEL.HINT:
        # Todo
        source = 'a = int(input())\nb = int(input())\nn = int(input())'
        code_info = CodeInfo(User())
        # hint_handler = HintHandler(graph, PathFinderV4, MeasuredTreeV3)
        # hint = hint_handler.get_hint(source, code_info)
        # print(hint.recommended_code)


def __run_test_system(path: str, task: TASK = TASK.PIES, to_construct: bool = True,
               to_serialize: bool = True, to_visualize: bool = True) -> None:
    graph = __construct_graph(path, task, to_construct, to_serialize, to_visualize)

    # It's possible not to include TEST_INPUT.RATE in dict, in this case it will be found by
    # running tests on TEST_INPUT.SOURCE_CODE.
    # However, to speed up the process, one may include TEST_INPUT.RATE.
    # Todo: get ages and experiences from args?
    ages = [12, 15, 18]
    experiences = [INT_EXPERIENCE.LESS_THAN_HALF_YEAR, INT_EXPERIENCE.FROM_ONE_TO_TWO_YEARS,
                   INT_EXPERIENCE.MORE_THAN_SIX]
    test_fragments = TestSystem.generate_all_test_fragments(ages, experiences, TestSystem.get_fragments_for_task(task))
    ts = TestSystem(test_fragments, task=task, add_same_docs=False, graph=graph)


def main() -> None:
    configure_logger(to_delete_previous_logs=True)
    __configure_args()
    args = parser.parse_args()
    path = args.path[0]
    if not os.path.exists(args.path[0]):
        log_and_raise_error(f'Path {path} does not exist', log)
    # Todo: do we want to add a slash if it's a file with serialized graph?
    path = add_slash(path)
    action = ACTIONS_TYPE(args.action[0])

    if action == ACTIONS_TYPE.PREPROCESSING:
        level = PREPROCESSING_LEVEL.get_level(args.level)
        __data_preprocessing(path, level)
    elif action == ACTIONS_TYPE.STATISTICS:
        # Todo
        pass
    elif action == ACTIONS_TYPE.ALGO:
        level = ALGO_LEVEL.get_level(args.level)
        task = __get_task(args.task)
        __run_algo(path, level, task, args.construct, args.serialize, args.viz)
    elif action == ACTIONS_TYPE.TEST_SYSTEM:
        task = __get_task(args.task)
        __run_test_system(path, task, args.construct, args.serialize, args.viz)
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
