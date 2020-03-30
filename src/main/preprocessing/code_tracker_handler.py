# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Union, Any, Tuple

import numpy as np
import pandas as pd

from src.main.util import consts
from src.main.util.file_util import get_extension_from_file
from src.main.util.language_util import get_language_by_extension
from src.main.util.strings_util import convert_camel_case_to_snake_case

log = logging.getLogger(consts.LOGGER_NAME)

# todo: find out a proper way to check for default values
def fill_column(data: pd.DataFrame, column: consts.CODE_TRACKER_COLUMN,
                default_value: consts.DEFAULT_VALUE) -> Any:
    values = data[column.value].unique()
    index = np.argwhere(default_value.is_equal(values))
    values = np.delete(values, index)
    if len(values) > 1:
        # It is an invalid file
        log.error('Invalid value for column!')
        return consts.INVALID_FILE_FOR_PREPROCESSING
    if len(values) == 1:
        return values[0]
    return default_value.value


# If we have a few languages, we return NOT_DEFINED, else we return the language.
# If all files have the same extension, then we return a language, which matches to this extension (it works for all
# languages for LANGUAGES_DICT from const file)
# For example, we have a set of files: a.py, b.py. The function returns python because we have one extension for all
# files.
# For a case: a.py, b.p and c.java the function returns NOT_DEFINED because the files have different extensions
def get_ct_language(data: pd.DataFrame) -> consts.LANGUAGE:
    values = data[consts.CODE_TRACKER_COLUMN.FILE_NAME.value].unique()
    extensions = set(map(get_extension_from_file, values))
    if len(extensions) == 1:
        return get_language_by_extension(extensions.pop())
    return consts.LANGUAGE.NOT_DEFINED


def handle_ct_file(ct_file: str) -> Tuple[pd.DataFrame, consts.LANGUAGE]:
    log.info(f'Start handling the file {ct_file}')
    ct_df = pd.read_csv(ct_file, encoding=consts.ISO_ENCODING)
    # It's easier to have all tasks written in snake case because further they will be used as folders names and so on
    ct_df[consts.CODE_TRACKER_COLUMN.CHOSEN_TASK.value] = ct_df[consts.CODE_TRACKER_COLUMN.CHOSEN_TASK.value].fillna(''). \
        apply(lambda t: convert_camel_case_to_snake_case(t))
    language = get_ct_language(ct_df)
    ct_df[consts.CODE_TRACKER_COLUMN.LANGUAGE.value] = language.value
    ct_df[consts.CODE_TRACKER_COLUMN.AGE.value] = fill_column(ct_df,
                                                              consts.CODE_TRACKER_COLUMN.AGE,
                                                              consts.DEFAULT_VALUE.AGE)
    ct_df[consts.CODE_TRACKER_COLUMN.EXPERIENCE.value] = fill_column(ct_df,
                                                                     consts.CODE_TRACKER_COLUMN.EXPERIENCE,
                                                                     consts.DEFAULT_VALUE.EXPERIENCE)
    return ct_df, language
