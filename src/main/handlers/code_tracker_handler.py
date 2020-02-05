from src.main.util import consts
import pandas as pd
import numpy as np
import logging

from src.main.util.file_util import get_extension_from_file
from src.main.util.language_util import get_language_by_extension

log = logging.getLogger(consts.LOGGER_NAME)


def profile_column_handler(data: pd.DataFrame, column: consts.CODE_TRACKER_COLUMN,
                           default_value: consts.DEFAULT_VALUES):
    values = data[column].unique()
    index = np.argwhere((values == default_value) | pd.isnull(values))
    if (index.shape[0] == 0 and len(values) > 1) or len(values) > 2:
        log.error('Invalid value for column!')
        # it is an invalid file
        return -1
    values = np.delete(values, index)
    if len(values) == 1:
        return values[0]
    return default_value


# If we have a few languages, we return NOT_DEFINED, else we return the language.
# If all files have the same extension, then we return a language, which matches to this extension (it works for all
# languages for LANGUAGES_DICT from const file)
# For example, we have a set of files: a.py, b.py. The function returns PYTHON because we have one extension for all
# files.
# For a case: a.py, b.p and c.java the function returns NOT_DEFINED because the files have different extensions
def get_ct_language(data: pd.DataFrame):
    values = data[consts.CODE_TRACKER_COLUMN.FILE_NAME.value].unique()
    extensions = set(map(get_extension_from_file, values))
    if len(extensions) == 1:
        return get_language_by_extension(extensions.pop())
    return consts.LANGUAGE.NOT_DEFINED.value
