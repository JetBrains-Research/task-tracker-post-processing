# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from enum import Enum
from contextlib import suppress
from typing import List, Dict, Any

from pandas import isna
from numpy import nan, datetime64, isnat


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class CODE_TRACKER_COLUMN(Enum):
    AGE = 'age'
    EXPERIENCE = 'programExperience'
    EXPERIENCE_YEARS = 'programExperienceYears'
    EXPERIENCE_MONTHS = 'programExperienceMonths'
    TASK_STATUS = 'taskStatus'
    GENDER = 'gender'
    COUNTRY = 'country'
    FILE_NAME = 'fileName'
    DATE = 'date'
    TIMESTAMP = 'timestamp'
    LANGUAGE = 'language'
    FRAGMENT = 'fragment'
    CHOSEN_TASK = 'chosenTask'
    TESTS_RESULTS = 'testsResults'
    INT_EXPERIENCE = 'intExperience'
    TEST_MODE = 'testMode'
    USER_ID = 'userId'

    def fits_restrictions(self, value: Any) -> bool:
        if self is CODE_TRACKER_COLUMN.AGE:
            return isinstance(value, float)
        elif self is CODE_TRACKER_COLUMN.EXPERIENCE:
            return str(value) in EXPERIENCE.values()
        # Todo: implement restrictions for other columns
        else:
            raise NotImplementedError(f"Cannot find any restrictions for {self}")

    @classmethod
    def get_columns_for_filling(cls) -> List['CODE_TRACKER_COLUMN']:
        return [cls.AGE, cls.EXPERIENCE_YEARS, cls.EXPERIENCE_MONTHS, cls.GENDER, cls.COUNTRY]


class TEST_MODE(Enum):
    ON = 'ON'
    OFF = 'OFF'


class TMP_COLUMN(Enum):
    SHIFTED_FRAGMENT = f'shift_{CODE_TRACKER_COLUMN.FRAGMENT.value}'
    DIFFS = 'diffs'
    SHIFTED_DIFFS = 'shift_diffs'



class ACTIVITY_TRACKER_COLUMN(Enum):
    TIMESTAMP_ATI = 'timestampAti'
    USERNAME = 'username'
    EVENT_TYPE = 'eventType'
    EVENT_DATA = 'eventData'
    PROJECT_NAME = 'project_name'
    FOCUSED_COMPONENT = 'focusedComponent'
    CURRENT_FILE = 'currentFile'
    PSI_PATH = 'PSIPath'
    EDITOR_LINE = 'editorLine'
    EDITOR_COLUMN = 'editorColumn'
    TASK = 'task',
    ATI_ID = 'atiId'

    @classmethod
    def activity_tracker_columns(cls) -> List[str]:
        return [cls.TIMESTAMP_ATI.value, cls.USERNAME.value, cls.EVENT_TYPE.value, cls.EVENT_DATA.value,
                cls.PROJECT_NAME.value, cls.FOCUSED_COMPONENT.value, cls.CURRENT_FILE.value, cls.PSI_PATH.value,
                cls.EDITOR_LINE.value, cls.EDITOR_COLUMN.value, cls.TASK.value]


class ACTIVITY_TRACKER_EVENTS(Enum):
    ACTION = 'Action'
    COMPILATION_FINISHED = 'CompilationFinished'

    @classmethod
    def action_events(cls) -> List[str]:
        return ['Run', 'Rerun', 'RunClass', 'DebugClass', 'ToggleLineBreakpoint', 'Debugger.AddToWatch', 'Debug',
                'Stop', 'Resume', 'StepInto', 'CompileDirty', 'EditorCopy', 'EditorPaste', 'EditorCut', 'ReformatCode',
                '$Undo', '$Paste', '$Copy', 'ChooseRunConfiguration', 'CopyElement', 'PasteElement', 'CutElement']


class DEFAULT_VALUE(Enum):
    AGE = 0
    EXPERIENCE = None
    INT_EXPERIENCE = -1
    TASK = None
    TASK_STATUS = None
    DATE = datetime64('NaT')
    EVENT_TYPE = None
    EVENT_DATA = None
    FRAGMENT = None

    # todo: add tests
    def is_equal(self, value) -> bool:
        # TypeError can be raised, for example, if 'int' value is passed to isnat()
        with suppress(TypeError):
            if self.value is nan:
                return isinstance(value, float) and isna(value)
            if isnat(self.value):
                return isnat(value)
        return self.value == value


class EXPERIENCE(Enum):
    LESS_THAN_HALF_YEAR = 'LESS_THAN_HALF_YEAR'
    FROM_HALF_TO_ONE_YEAR = 'FROM_HALF_TO_ONE_YEAR'
    FROM_ONE_TO_TWO_YEARS = 'FROM_ONE_TO_TWO_YEARS'
    FROM_TWO_TO_FOUR_YEARS = 'FROM_TWO_TO_FOUR_YEARS'
    FROM_FOUR_TO_SIX_YEARS = 'FROM_FOUR_TO_SIX_YEARS'
    MORE_THAN_SIX = 'MORE_THAN_SIX'

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for _, member in EXPERIENCE.__members__.items()]

    @classmethod
    def sorted_values(cls) -> List[str]:
        return [
            cls.LESS_THAN_HALF_YEAR.value,
            cls.FROM_HALF_TO_ONE_YEAR.value,
            cls.FROM_ONE_TO_TWO_YEARS.value,
            cls.FROM_TWO_TO_FOUR_YEARS.value,
            cls.FROM_FOUR_TO_SIX_YEARS.value,
            cls.MORE_THAN_SIX.value
        ]


class INT_EXPERIENCE(Enum):
    LESS_THAN_HALF_YEAR = 0
    FROM_HALF_TO_ONE_YEAR = 1
    FROM_ONE_TO_TWO_YEARS = 2
    FROM_TWO_TO_FOUR_YEARS = 3
    FROM_FOUR_TO_SIX_YEARS = 4
    MORE_THAN_SIX = 5

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for _, member in INT_EXPERIENCE.__members__.items()]

    def get_short_str(self) -> str:
        if self is INT_EXPERIENCE.LESS_THAN_HALF_YEAR:
            return '< 0.5'
        elif self is INT_EXPERIENCE.FROM_HALF_TO_ONE_YEAR:
            return '0.5 - 1'
        elif self is INT_EXPERIENCE.FROM_ONE_TO_TWO_YEARS:
            return '1 - 2'
        elif self is INT_EXPERIENCE.FROM_TWO_TO_FOUR_YEARS:
            return '2 - 4'
        elif self is INT_EXPERIENCE.FROM_FOUR_TO_SIX_YEARS:
            return '4 - 6'
        elif self is INT_EXPERIENCE.MORE_THAN_SIX:
            return '> 6'
        else:
            raise NotImplementedError

    def get_str_experience(self) -> str:
        return EXPERIENCE.values()[self.value]


class TASK(Enum):
    PIES = 'pies'
    MAX_3 = 'max_3'
    ZERO = 'is_zero'
    VOTING = 'voting'
    BRACKETS = 'brackets'
    MAX_DIGIT = 'max_digit'

    @classmethod
    def tasks(cls) -> List['TASK']:
        return [task for task in TASK]

    @classmethod
    def tasks_values(cls) -> List[str]:
        return [member.value for _, member in TASK.__members__.items()]


class TASK_STATUS(Enum):
    SOLVED = 'SOLVED'
    NOT_SOLVED = 'NOT_SOLVED'


class TASKS_TESTS(Enum):
    TASKS_TESTS_PATH = ROOT_DIR + '/../../resources/tasks_tests/'
    SOURCE_OBJECT_NAME = 'source'
    INPUT_FILE_NAME = 'in'


class LANGUAGE(Enum):
    JAVA = 'java'
    PYTHON = 'python'
    KOTLIN = 'kotlin'
    CPP = 'cpp'
    UNDEFINED = 'undefined'


class TEST_RESULT(Enum):
    INCORRECT_CODE = -1
    LANGUAGE_UNDEFINED = -2
    # It can be incorrect although, but our checking tools cannot find any errors
    CORRECT_CODE = 0
    # It means that all tests are passed
    FULL_SOLUTION = 1


class FILE_SYSTEM_ITEM(Enum):
    PATH = 0
    SUBDIR = 1
    FILE = 2


INVALID_FILE_FOR_PREPROCESSING = -1


# Make sure all extensions (except an empty one) have a dot
# to be consistent with extensions getting in 'os.path' module
class EXTENSION(Enum):
    EMPTY = ''
    CSV = '.csv'
    PNG = '.png'
    HTML = '.html'
    TXT = '.txt'
    OUT = '.out'
    JAR = '.jar'
    PICKLE = '.pickle'
    PY = '.py'
    JAVA = '.java'
    KT = '.kt'
    CPP = '.cpp'
    DOT = '.dot'
    MD = '.md'
    GRADLE = '.gradle'


EXTENSION_TO_LANGUAGE_DICT: Dict[EXTENSION, LANGUAGE] = {
    EXTENSION.PY: LANGUAGE.PYTHON,
    EXTENSION.JAVA: LANGUAGE.JAVA,
    EXTENSION.KT: LANGUAGE.KOTLIN,
    EXTENSION.CPP: LANGUAGE.CPP,
    EXTENSION.EMPTY: LANGUAGE.UNDEFINED
}


class SPLIT(Enum):
    INDEX = 'index'
    RATE = 'rate'
    TASKS = 'tasks'


LOGGER_FILE = ROOT_DIR + '../../../../logs.log'
LOGGER_NAME = 'main_logger'

LOGGER_TEST_FILE = ROOT_DIR + '../../../../test_logs.log'

LOGGER_FORMAT = '%(asctime)s:%(levelname)s ==> %(message)s'

PATH_CMD_ARG = '-path'
ISO_ENCODING = 'ISO-8859-1'
UTF_ENCODING = 'utf8'

PYLINT_KEY_WORDS = ['Statement seems to have no effect']

ATI_DATA_FOLDER = 'ati_'
DI_DATA_FOLDER = 'di_'
ACTIVITY_TRACKER_FILE_NAME = 'ide-events'

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
MAX_DIF_SEC = 0.5

RESOURCES_PATH = ROOT_DIR + '/../../resources/'
TEST_DATA_PATH = RESOURCES_PATH + 'test_data'
TEST_PATH = ROOT_DIR + '/../../test'

GRAPH_REPRESENTATION_PATH = os.path.join(RESOURCES_PATH, 'graph_representation')
SERIALIZED_GRAPH_PATH = os.path.join(RESOURCES_PATH, 'serialized_graph')
SOLUTION_SPACE_TEST_RESULT_PATH = os.path.join(RESOURCES_PATH, 'solution_space')
CLI_PATH = os.path.join(ROOT_DIR + '/../', 'cli')

MERGING_CT_AND_ATI_OUTPUT_DIRECTORY = 'merged_ct_and_ati_result'
STATISTICS_OUTPUT_DIRECTORY = 'statistics_result'
PREPROCESSING_DIRECTORY = 'preprocessing_result'

# Todo: use zip
GUMTREE_PATH = os.path.join(RESOURCES_PATH, 'gumtree/bin/gumtree')

# v 2.0 - with stopping after the first break
# v 3.0 - with java package detecting
RUNNING_TESTS_OUTPUT_DIRECTORY = 'running_tests_result_3'

MAX_DIFF_SYMBOLS = 30

TIMEOUT = 5

TRUE_VALUES_SET = {'true', 't', '1', 'yes', 'y'}
FALSE_VALUES_SET = {'false', 'f', '0', 'no', 'n'}
