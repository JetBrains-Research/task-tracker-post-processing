# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
import subprocess
import pandas as pd

from src.main.util import consts
from src.main.util.consts import LOGGER_NAME
from src.main.preprocessing.util import handle_folder
from src.main.util.file_util import create_file, remove_file

log = logging.getLogger(LOGGER_NAME)


FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value


def __does_have_errors(output: str) -> bool:
    for k_w in consts.PYLINT_KEY_WORDS:
        if k_w in output:
            return True
    return False


def __check_source_with_pylint(source: str) -> bool:
    # If the source is nan we don't need to check code
    if consts.DEFAULT_VALUE.FRAGMENT.is_equal(source):
        return False

    file_path = os.path.join(consts.RESOURCES_PATH, 'tmp' + consts.EXTENSION.PY.value)
    create_file(source, file_path)
    args = ['pylint', file_path]
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    output = p.communicate()[0].decode(consts.UTF_ENCODING)
    p.kill()
    remove_file(file_path)

    return __does_have_errors(output)


def __handle_df(df: pd.DataFrame) -> pd.DataFrame:
    i = 0
    need_to_remove = []
    while i < df.shape[0]:
        if __check_source_with_pylint(df[FRAGMENT].iloc[i]):
            need_to_remove.append(i)
        i += 1
    return df.drop(need_to_remove)


def remove_pylint_checker_errors(path: str, result_folder_prefix: str = 'remove_pylint_checker_errors') -> str:
    return handle_folder(path, result_folder_prefix, __handle_df)
