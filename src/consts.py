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

NOT_DEFINED_LANGUAGE = 'NOT_DEFINED'
ENCODING = 'ISO-8859-1'
