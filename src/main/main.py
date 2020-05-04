# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import sys
import logging

import pandas as pd

from src.main.util import consts
from src.main.util.file_util import add_slash
from src.main.util.log_util import configure_logger
from src.main.solution_space.hint import HintHandler
from src.main.util.consts import PATH_CMD_ARG, TASK, EXPERIENCE
from src.main.solution_space.data_classes import User, CodeInfo
from src.main.preprocessing.preprocessing import preprocess_data
from src.main.splitting.splitting import split_tasks_into_separate_files
from src.main.solution_space.path_finder.path_finder_v_2 import PathFinderV2
from src.main.solution_space.path_finder_test_system import TestSystem, TEST_INPUT
from src.main.solution_space.solution_space_handler import construct_solution_graph
from src.main.solution_space.solution_space_visualizer import SolutionSpaceVisualizer
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer
from src.main.preprocessing.intermediate_diffs_removing import remove_intermediate_diffs
from src.main.solution_space.measured_vertex.measured_vertex_v_1 import MeasuredVertexV1
from src.main.preprocessing.inefficient_statements_removing import remove_inefficient_statements

pd.set_option('display.max_rows', 250)
pd.set_option('display.max_columns', 100)

log = logging.getLogger(consts.LOGGER_NAME)


def __get_data_path() -> str:
    args = sys.argv
    path = args[args.index(PATH_CMD_ARG) + 1]
    if not os.path.isdir(path):
        log.error(f'It is not a folder, passed path is {path}')
        sys.exit(1)
    return add_slash(path)


def main() -> None:
    configure_logger()
    path = __get_data_path()

    """
    Data preprocessing
    """
    # preprocess_data(path)

    """
    Tasks separating
    Note: Path should contain files after preprocessing with tests results
    """
    # split_tasks_into_separate_files(path)

    """
    Graph constructing
    """
    graph = construct_solution_graph(path, TASK.PIES, to_store_dist=False)
    print('Graph was constructed')

    """
    Graph serialization
    # """
    # path = SolutionSpaceSerializer.serialize(graph, serialized_file_prefix='serialized_graph_with_dist')
    # print(f'Serialized path: {path}')
    # new_graph = SolutionSpaceSerializer.deserialize(path)
    # print(str(graph) == str(new_graph))

    """
    Graph visualization
    """
    # gv = SolutionSpaceVisualizer(graph)
    # graph_representation_path = gv.create_graph_representation(name_prefix='graph_all_space_without_helper_folding')
    # print(graph_representation_path)

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
    # test_fragments = [{TEST_INPUT.SOURCE_CODE: 'a = int(input())',
    #                    TEST_INPUT.AGE: 17,
    #                    TEST_INPUT.EXPERIENCE: EXPERIENCE.LESS_THAN_HALF_YEAR},
    #                   {TEST_INPUT.SOURCE_CODE: 'a = int(input())\nb = int(input())',
    #                    TEST_INPUT.AGE: 12,
    #                    TEST_INPUT.EXPERIENCE: EXPERIENCE.FROM_ONE_TO_TWO_YEARS}]
    #
    # ts = TestSystem(test_fragments)


if __name__ == '__main__':
    main()
