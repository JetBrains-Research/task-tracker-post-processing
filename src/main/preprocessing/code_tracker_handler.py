# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Any, Tuple, Callable

import numpy as np
import pandas as pd

from src.main.util.file_util import get_extension_from_file
from src.main.util.language_util import get_language_by_extension
from src.main.util.strings_util import convert_camel_case_to_snake_case
from src.main.util.consts import CODE_TRACKER_COLUMN, DEFAULT_VALUE, INVALID_FILE_FOR_PREPROCESSING, LANGUAGE, \
    ISO_ENCODING, LOGGER_NAME, TEST_MODE

log = logging.getLogger(LOGGER_NAME)


def fill_column(data: pd.DataFrame, column: CODE_TRACKER_COLUMN, fits_column_restriction: Callable[[Any], bool],
                default_value: DEFAULT_VALUE) -> Any:
    values = data[column.value].unique()
    index = np.argwhere(np.array(list(map(default_value.is_equal, values))))
    values = np.delete(values, index)
    # If list is empty after removing defaults, return default value
    if values.size == 0:
        return default_value.value
    # If we have only 1 valid element after removing defaults, we should return it
    elif len(values) == 1 and fits_column_restriction(values[0]):
        return values[0]
    # Otherwise, list can have 1 invalid element, or more than 1 element
    # Both these cases are incorrect, so we should return INVALID_FILE_FOR_PREPROCESSING
    log.error('Invalid value for column!')
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
    # It's easier to have all tasks written in snake case because further they will be used as folders names and so on
    ct_df[CODE_TRACKER_COLUMN.CHOSEN_TASK.value] = ct_df[CODE_TRACKER_COLUMN.CHOSEN_TASK.value].fillna(
        ''). \
        apply(lambda t: convert_camel_case_to_snake_case(t))
    language = get_ct_language(ct_df)
    ct_df[CODE_TRACKER_COLUMN.LANGUAGE.value] = language.value
    ct_df[CODE_TRACKER_COLUMN.AGE.value] = fill_column(ct_df,  CODE_TRACKER_COLUMN.AGE,
                                                       CODE_TRACKER_COLUMN.AGE.fits_restrictions, DEFAULT_VALUE.AGE)
    ct_df[CODE_TRACKER_COLUMN.EXPERIENCE.value] = fill_column(ct_df, CODE_TRACKER_COLUMN.EXPERIENCE,
                                                              CODE_TRACKER_COLUMN.EXPERIENCE.fits_restrictions,
                                                              DEFAULT_VALUE.EXPERIENCE)
    return ct_df, language

