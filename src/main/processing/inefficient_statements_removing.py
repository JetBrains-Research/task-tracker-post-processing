# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import tempfile
import subprocess

import pandas as pd

from src.main.util import consts
from src.main.util.data_util import handle_folder
from src.main.util.log_util import log_and_raise_error
from src.main.util.consts import LOGGER_NAME, FILE_SYSTEM_ITEM
from src.main.util.strings_util import contains_any_of_substrings
from src.main.util.file_util import get_all_file_system_items, language_item_condition, get_output_directory

log = logging.getLogger(LOGGER_NAME)

FRAGMENT = consts.TASK_TRACKER_COLUMN.FRAGMENT.value
LANGUAGE = consts.TASK_TRACKER_COLUMN.LANGUAGE.value


def __has_inefficient_statements(source: str) -> bool:
    # If the source is nan we don't need to check code
    if consts.DEFAULT_VALUE.FRAGMENT.is_equal(source):
        return False

    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(bytes(str(source), encoding=consts.UTF_ENCODING))
        tmp.seek(0)

        args = ['pylint', tmp.name]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        output = p.communicate()[0].decode(consts.UTF_ENCODING)
        p.kill()

        return contains_any_of_substrings(output, consts.PYLINT_KEY_WORDS)


def __get_language(df: pd.DataFrame) -> consts.LANGUAGE:
    languages = df[LANGUAGE].unique()
    if len(languages) != 1:
        log_and_raise_error(f'Dataframe has {len(languages)} unique values!', log)
    try:
        return consts.LANGUAGE(languages[0])
    except ValueError:
        log_and_raise_error(f'Unknown language key: {languages[0]}', log)


def remove_inefficient_statements_from_df(df: pd.DataFrame) -> pd.DataFrame:
    # This function supports only Python language
    if __get_language(df) != consts.LANGUAGE.PYTHON:
        return df
    return df[df.apply(lambda row: not __has_inefficient_statements(row[FRAGMENT]), axis=1)]


def remove_inefficient_statements(path: str, output_directory_prefix: str = 'remove_inefficient_statements') -> str:
    """
    This module allows to remove inefficient statements in the files. We use pylint library to detect such kinds of
    statements. For example, in the code fragment:

    a = input()
    print

    the statement print is an inefficient statement.

    Note: available only for Python language.

    For more details see
    https://github.com/JetBrains-Research/task-tracker-post-processing/wiki/Data-processing:-remove-inefficient-statements
    """
    languages = get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
    output_directory = get_output_directory(path, output_directory_prefix)
    for _ in languages:
        handle_folder(path, output_directory_prefix, remove_inefficient_statements_from_df)
    return output_directory
