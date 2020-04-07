# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
import pandas as pd
from collections import Callable

from src.main.util import consts
from src.main.util.consts import LOGGER_NAME, ISO_ENCODING
from src.main.util.file_util import get_all_file_system_items, extension_file_condition, get_result_folder, \
    write_result


log = logging.getLogger(LOGGER_NAME)


def handle_folder(path: str, result_folder_prefix: str, handle_df: Callable) -> str:
    result_folder = get_result_folder(path, result_folder_prefix)
    files = get_all_file_system_items(path, extension_file_condition(consts.EXTENSION.CSV))
    for file in files:
        df = pd.read_csv(file, encoding=ISO_ENCODING)
        df = handle_df(df)
        write_result(result_folder, path, file, df)
    return result_folder
