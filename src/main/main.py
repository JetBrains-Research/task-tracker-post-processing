import logging
import os
import sys

import pandas as pd

from src.main.util.file_util import add_slash
from src.main.preprocessing.preprocessing import preprocess_data
from src.main.util import consts
from src.main.util.consts import PATH_CMD_ARG

pd.set_option('display.max_rows', 250)
pd.set_option('display.max_columns', 100)

log = logging.getLogger(consts.LOGGER_NAME)


def __get_data_path():
    args = sys.argv
    path = args[args.index(PATH_CMD_ARG) + 1]
    if not os.path.isdir(path):
        log.error("It's not a folder, passed path is " + path)
        sys.exit(1)
    path = add_slash(path)
    return path


def main():
    logging.basicConfig(filename=consts.LOGGER_FILE, level=logging.INFO)
    path = __get_data_path()

    # preprocess data before splitting
    preprocess_data(path)


if __name__ == "__main__":
    main()
