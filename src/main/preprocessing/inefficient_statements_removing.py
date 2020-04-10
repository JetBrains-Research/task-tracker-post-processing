# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
import tempfile
import subprocess
import pandas as pd

from src.main.util import consts
from src.main.util.consts import LOGGER_NAME
from src.main.util.data_util import handle_folder
from src.main.util.file_util import create_file, remove_file
from src.main.util.strings_util import contains_any_of_substrings

log = logging.getLogger(LOGGER_NAME)


FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value


def __has_inefficient_statements(source: str) -> bool:
    # If the source is nan we don't need to check code
    if consts.DEFAULT_VALUE.FRAGMENT.is_equal(source):
        return False

    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(bytes(source, encoding=consts.UTF_ENCODING))
        tmp.seek(0)

        args = ['pylint', tmp.name]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        output = p.communicate()[0].decode(consts.UTF_ENCODING)
        p.kill()

        return contains_any_of_substrings(output, consts.PYLINT_KEY_WORDS)


def __remove_inefficient_statements_from_df(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.apply(lambda row: not __has_inefficient_statements(row[FRAGMENT]), axis=1)]


def remove_inefficient_statements(path: str, result_folder_prefix: str = 'remove_pylint_checker_errors') -> str:
    return handle_folder(path, result_folder_prefix, __remove_inefficient_statements_from_df)
