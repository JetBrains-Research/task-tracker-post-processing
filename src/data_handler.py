import pandas as pd
import numpy as np
from src import consts


# Todo: add logger


def profile_column_handler(data: pd.DataFrame, column: consts.CODE_TRACKER_COLUMN, default_value: consts.DEFAULT_VALUES):
    values = data[column].unique()
    index = np.argwhere((values == default_value) | pd.isnull(values))
    if (index.shape[0] == 0 and len(values) > 1) or len(values) > 2:
        # it is an invalid file
        return -1
    values = np.delete(values, index)
    if len(values) == 1:
        return values[0]
    return default_value


def __get_extension(file_name: str):
    parts = file_name.split(".")
    return parts[-1]


def __get_language_name(extension: str):
    return consts.LANGUAGES_DICT.get(extension, consts.NOT_DEFINED_LANGUAGE)


# If we have a few languages, we return NOT_DEFINED, else we return the language.
# If all files have the same extension, then we return a language, which matches to this extension (it works for all
# languages for LANGUAGES_DICT from const file)
# For example, we have a set of files: a.py, b.py. The function returns PYTHON because we have one extension for all
# files.
# For a case: a.py, b.p and c.java the function returns NOT_DEFINED because the files have different extensions
def get_language(data: pd.DataFrame):
    values = data[consts.CODE_TRACKER_COLUMN.FILE_NAME.value].unique()
    extensions = set(map(__get_extension, values))
    if len(extensions) == 1:
        return __get_language_name(extensions.pop())
    return consts.NOT_DEFINED_LANGUAGE


# Get new column with languages for each row from dataset
def get_language_column(data: pd.DataFrame):
    languages = []
    for _, row in data.iterrows():
        languages.append(__get_language_name(__get_extension(row[consts.CODE_TRACKER_COLUMN.FILE_NAME.value])))
    return languages

