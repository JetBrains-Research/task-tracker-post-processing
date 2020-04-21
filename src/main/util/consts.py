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
    FILE_NAME = 'fileName'
    DATE = 'date'
    TIMESTAMP = 'timestamp'
    LANGUAGE = 'language'
    FRAGMENT = 'fragment'
    CHOSEN_TASK = 'chosenTask'
    TASK_STATUS = 'taskStatus'
    TESTS_RESULTS = 'testsResults'

    def fits_restrictions(self, value: Any) -> bool:
        if self is CODE_TRACKER_COLUMN.AGE:
            return isinstance(value, float)
        elif self is CODE_TRACKER_COLUMN.EXPERIENCE:
            return str(value) in EXPERIENCE.values()
        # Todo: implement restrictions for other columns
        else:
            raise NotImplementedError(f"Cannot find any restrictions for {self}")


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
    EXPERIENCE = nan
    TASK = nan
    TASK_STATUS = nan
    DATE = datetime64('NaT')
    EVENT_TYPE = nan
    EVENT_DATA = nan
    FRAGMENT = nan

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


class TASK(Enum):
    PIES = 'pies'
    MAX_3 = 'max_3'
    ZERO = 'is_zero'
    ELECTION = 'election'
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
    NOT_DEFINED = 'not_defined'


class TEST_RESULT(Enum):
    INCORRECT_CODE = -1
    LANGUAGE_NOT_DEFINED = -2
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


EXTENSION_TO_LANGUAGE_DICT: Dict[EXTENSION, LANGUAGE] = {
    EXTENSION.PY: LANGUAGE.PYTHON,
    EXTENSION.JAVA: LANGUAGE.JAVA,
    EXTENSION.KT: LANGUAGE.KOTLIN,
    EXTENSION.CPP: LANGUAGE.CPP,
    EXTENSION.EMPTY: LANGUAGE.NOT_DEFINED
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

GRAPH_REPRESENTATION_PATH = RESOURCES_PATH + 'graph_representation'
SOLUTION_SPACE_TEST_RESULT_PATH = RESOURCES_PATH + 'solution_space'

PREPROCESSING_RESULT_FOLDER = 'preprocessing_result'
STATISTICS_RESULT_FOLDER = 'statistics_result'

# Todo: use zip
GUMTREE_PATH = RESOURCES_PATH + 'gumtree/bin/gumtree'

# v 2.0 - with stopping after the first break
# v 3.0 - with java package detecting
RUNNING_TESTS_RESULT_FOLDER = 'running_tests_result_3'

MAX_DIFF_SYMBOLS = 30

TIMEOUT = 5
