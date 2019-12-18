from enum import Enum
import numpy as np


class COLUMN(Enum):
    AGE = 'age'
    EXPERIENCE = 'programExperience'
    FILE_NAME = 'fileName'


class DEFAULT_VALUES(Enum):
    AGE = 0
    EXPERIENCE = np.nan


LANGUAGES_DICT = {
    'py': 'PYTHON',
    'java': 'JAVA',
    'kt': 'KOTLIN',
}

LOGGER_FILE = '../logs.log'
LOGGER_NAME = 'main_logger'

PATH_CMD_ARG = '-path'
ENCODING = 'ISO-8859-1'

ACTIVITY_TRACKER_FOLDER_NAME = 'ati'
ACTIVITY_TRACKER_FILE_NAME = 'ide-events'

NOT_DEFINED_LANGUAGE = 'NOT_DEFINED'
