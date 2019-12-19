from enum import Enum
import numpy as np


class COLUMN(Enum):
    AGE = 'age'
    EXPERIENCE = 'programExperience'
    FILE_NAME = 'fileName'
    DATE = 'date'
    TIMESTAMP = 'timestamp'
    TIMESTAMP_ATI = 'timestamp_ati'
    USERNAME = 'username'
    EVENT_TYPE = 'eventType'
    EVENT_DATA = 'eventData'
    PROJECT_NAME = 'project_name'
    FOCUSED_COMPONENT = 'focusedComponent'
    CURRENT_FILE = 'currentFile'
    PSI_PATH = 'PSIPath'
    EDITOR_LINE = 'editorLine'
    EDITOR_COLUMN = 'editorColumn'
    TASK = 'task'


class DEFAULT_VALUES(Enum):
    AGE = 0
    EXPERIENCE = np.nan


class ACTIVITY_TRACKER_EVENTS(Enum):
    ACTION = 'Action'
    COMPILATION_FINISHED = 'CompilationFinished'


ACTION_EVENTS = ['Run', 'Rerun', 'RunClass', 'DebugClass', 'ToggleLineBreakpoint', 'Debugger.AddToWatch', 'Debug',
                 'Stop', 'Resume', 'StepInto', 'CompileDirty', 'EditorCopy', 'EditorPaste', 'EditorCut', 'ReformatCode',
                 '$Undo', '$Paste', '$Copy']

ACTIVITY_TRACKER_COLUMNS = [COLUMN.TIMESTAMP_ATI.value, COLUMN.USERNAME.value, COLUMN.EVENT_TYPE.value,
                            COLUMN.EVENT_DATA.value, COLUMN.PROJECT_NAME.value, COLUMN.FOCUSED_COMPONENT.value,
                            COLUMN.CURRENT_FILE.value, COLUMN.PSI_PATH.value, COLUMN.EDITOR_LINE.value,
                            COLUMN.EDITOR_COLUMN.value, COLUMN.TASK.value]

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

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
MAX_DIF_SEC = 30
