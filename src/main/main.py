# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import sys
import logging

import pandas as pd

from src.main.solution_space.data_classes import User
from src.main.solution_space.hint import HintGetter
from src.main.solution_space.solution_space_handler import construct_solution_graph
from src.main.util import consts
from src.main.util.file_util import add_slash, serialize_data_and_write_to_file, deserialize_data_from_file
from src.main.util.consts import PATH_CMD_ARG, LOGGER_FORMAT, TASK
from src.main.preprocessing.preprocessing import preprocess_data
from src.main.splitting.splitting import split_tasks_into_separate_files


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
    logging.basicConfig(filename=consts.LOGGER_FILE, format=LOGGER_FORMAT, level=logging.INFO)
    path = __get_data_path()

    # Preprocess data before splitting
    # preprocess_data(path)

    # Path should contain files after preprocessing with tests results
    # split_tasks_into_separate_files(path)

    source = 'a = int(input())\nb = int(input())'
    user = User()

    # graph = deserialize_data_from_file(f'/home/elena/workspaces/python/codetracker-data/data/pies_solution_graph{consts.EXTENSION.PICKLE.value}')
    # serialize_data_and_write_to_file(f'/home/elena/workspaces/python/codetracker-data/data/pies_solution_graph{consts.EXTENSION.PICKLE.value}', graph)

    graph = construct_solution_graph(path, TASK.PIES)
    goals = graph.end_vertex.parents
    print(f'goals are {goals}')

    # hint_getter = HintGetter(graph)
    # hint = hint_getter.get_hint(source, user)
    # print(hint.recomennded_code)



if __name__ == '__main__':
    main()
