import pandas as pd
import numpy as np
from src import consts


def profile_column_handler(data, column, default_value):
    values = data[column].unique()
    index = np.argwhere((values == default_value) | pd.isnull(values))
    if (index.shape[0] == 0 and len(values) > 1) or len(values) > 2:
        # it is a invalid file
        return -1
    values = np.delete(values, index)
    if len(values) == 1:
        return values[0]
    return default_value


def __get_extension(file_name):
    parts = file_name.split(".")
    return parts[len(parts) - 1]


def __get_language_name(extension):
    if consts.LANGUAGES_DICT.get(extension):
        return consts.LANGUAGES_DICT[extension]
    return consts.NOT_DEFINED_LANGUAGE


# if we have note 1 language, we return NOT_DEFINED
# Get 1 language for all files
def get_language(data):
    values = data[consts.COLUMN.FILE_NAME.value].unique()
    extensions = list(map(__get_extension, values))
    if len(extensions) == 1:
        return __get_language_name(extensions[0])
    return consts.NOT_DEFINED_LANGUAGE


# get new column with languages for each row from dataset
def get_language_column(data):
    languages = []
    for index, row in data.iterrows():
        languages.append(__get_language_name(__get_extension(row[consts.COLUMN.FILE_NAME.value])))
    return languages

