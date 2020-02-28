import os
from numpy import nan
from enum import Enum

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
    def activity_tracker_columns(cls):
        return [cls.TIMESTAMP_ATI.value, cls.USERNAME.value, cls.EVENT_TYPE.value, cls.EVENT_DATA.value,
                cls.PROJECT_NAME.value, cls.FOCUSED_COMPONENT.value, cls.CURRENT_FILE.value, cls.PSI_PATH.value,
                cls.EDITOR_LINE.value, cls.EDITOR_COLUMN.value, cls.TASK.value]


class ACTIVITY_TRACKER_EVENTS(Enum):
    ACTION = 'Action'
    COMPILATION_FINISHED = 'CompilationFinished'

    @classmethod
    def action_events(cls):
        return ['Run', 'Rerun', 'RunClass', 'DebugClass', 'ToggleLineBreakpoint', 'Debugger.AddToWatch', 'Debug',
                'Stop', 'Resume', 'StepInto', 'CompileDirty', 'EditorCopy', 'EditorPaste', 'EditorCut', 'ReformatCode',
                '$Undo', '$Paste', '$Copy', 'ChooseRunConfiguration', 'CopyElement', 'PasteElement', 'CutElement']


class DEFAULT_VALUES(Enum):
    AGE = 0
    EXPERIENCE = nan


class TASK(Enum):
    PIES = 'pies'
    MAX_3 = 'max_3'
    ZERO = 'zero'
    ELECTION = 'election'
    BRACKETS = 'brackets'
    MAX_DIGIT = 'max_digit'


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


class FILE_SYSTEM_ITEM(Enum):
    PATH = 0
    SUBDIR = 1
    FILE = 2


# add the dot to extensions to be consistent with extensions getting in 'os.path' module
EXTENSION_TO_LANGUAGE_DICT = {
    '.py': LANGUAGE.PYTHON.value,
    '.java': LANGUAGE.JAVA.value,
    '.kt': LANGUAGE.KOTLIN.value,
    '.cpp': LANGUAGE.CPP.value,
    '': LANGUAGE.NOT_DEFINED.value
}


class SPLIT_DICT(Enum):
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

ATI_DATA_FOLDER = 'ati_'
DI_DATA_FOLDER = 'di_'
ACTIVITY_TRACKER_FILE_NAME = 'ide-events'

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
MAX_DIF_SEC = 0.5

TEST_DATA_PATH = ROOT_DIR + '/../../resources/test_data'
TEST_PATH = ROOT_DIR + '/../../test'

PREPROCESSING_RESULT_FOLDER = 'preprocessing_result'
STATISTICS_RESULT_FOLDER = 'statistics_result'

# v 2.0 - with stopping after the first break
# v 3.0 - with java package detecting
RUNNING_TESTS_RESULT_FOLDER = 'running_tests_result_3'

MAX_DIFF_SYMBOLS = 30

SUBPROCESS_TIMEOUT = 5
