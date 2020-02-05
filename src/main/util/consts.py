import os
import numpy as np
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
    EXPERIENCE = np.nan


class TASKS_TESTS(Enum):
    TASKS_TESTS_PATH = ROOT_DIR + '/../../resources/tasks_tests/'
    SOURCE_FILE_NAME = 'source'
    TASKS = ['pies', 'max_3', 'zero', 'election', 'brackets', 'max_digit']
    INPUT_FILE_NAME = 'in'


class LANGUAGE(Enum):
    JAVA = 'JAVA'
    PYTHON = 'PYTHON'
    KOTLIN = 'KOTLIN'
    CPP = 'CPP'
    NOT_DEFINED = 'NOT_DEFINED'


EXTENSION_TO_LANGUAGE_DICT = {
    'py': LANGUAGE.PYTHON.value,
    'java': LANGUAGE.JAVA.value,
    'kt': LANGUAGE.KOTLIN.value,
    'cpp': LANGUAGE.CPP.value
}

LOGGER_FILE = '../../../../logs.log'
LOGGER_NAME = 'main_logger'

LOGGER_TEST_FILE = '../../../test_logs.log'

PATH_CMD_ARG = '-path'
ENCODING = 'ISO-8859-1'

ACTIVITY_TRACKER_FOLDER_NAME = 'ati'
ACTIVITY_TRACKER_FILE_NAME = 'ide-events'

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
MAX_DIF_SEC = 0.5

TEST_DATA_PATH = ROOT_DIR + '/../../resources/test_data'

RESULT_FOLDER = 'result'

MAX_DIFF_SYMBOLS = 30


