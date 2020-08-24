# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Any, Tuple, List

import numpy as np
import pandas as pd

from src.main.util.file_util import get_extension_from_file
from src.main.util.language_util import get_language_by_extension
from src.main.util.consts import CODE_TRACKER_COLUMN, INVALID_FILE_FOR_PREPROCESSING, LANGUAGE, \
    ISO_ENCODING, LOGGER_NAME

log = logging.getLogger(LOGGER_NAME)


def delete_default_values(values: List[Any], default_value: int = -1) -> List[Any]:
    return [x for x in values if x not in [np.nan, None, np.datetime64('NaT'),
                                             default_value, str(default_value)] and not pd.isna(x)]


def fill_column(data: pd.DataFrame, column: CODE_TRACKER_COLUMN, default_value: int = -1) -> Any:
    values = data[column.value].unique()
    # Delete all possible NONE values and default_value
    values = delete_default_values(values, default_value)
    if len(values) == 0:
        return default_value
    if len(values) == 1:
        return values[0]
    log.info('Invalid value for column!')
    return INVALID_FILE_FOR_PREPROCESSING


# If we have a few languages, we return UNDEFINED, else we return the language.
# If all files have the same extension, then we return a language, which matches to this extension (it works for all
# languages for LANGUAGES_DICT from const file)
# For example, we have a set of files: a.py, b.py. The function returns python because we have one extension for all
# files.
# For a case: a.py, b.p and c.java the function returns UNDEFINED because the files have different extensions
def get_ct_language(data: pd.DataFrame) -> LANGUAGE:
    values = data[CODE_TRACKER_COLUMN.FILE_NAME.value].unique()
    extensions = set(map(get_extension_from_file, values))
    if len(extensions) == 1:
        return get_language_by_extension(extensions.pop())
    return LANGUAGE.UNDEFINED


def handle_ct_file(ct_file: str) -> Tuple[pd.DataFrame, LANGUAGE]:
    log.info(f'Start handling the file {ct_file}')
    ct_df = pd.read_csv(ct_file, encoding=ISO_ENCODING)
    language = get_ct_language(ct_df)
    ct_df[CODE_TRACKER_COLUMN.LANGUAGE.value] = language.value

    for column in CODE_TRACKER_COLUMN.get_columns_for_filling():
        ct_df[column.value] = fill_column(ct_df, column)
    return ct_df, language

