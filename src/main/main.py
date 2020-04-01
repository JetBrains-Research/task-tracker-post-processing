# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import sys
import logging

import pandas as pd

from src.main.util import consts
from src.main.util.file_util import add_slash
from src.main.util.consts import PATH_CMD_ARG, LOGGER_FORMAT
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
    preprocess_data(path)

    # Path should contain files after preprocessing with tests results
    split_tasks_into_separate_files(path)


if __name__ == '__main__':
    main()
