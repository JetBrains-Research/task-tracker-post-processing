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
    EXPERIENCE = np.nan


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

LANGUAGE_TO_MIN_SYMBOLS = {
    # a = int(input())
    # print(a)
    LANGUAGE.PYTHON.value: 25,

    # class A{
    # public static void main(String args[]){
    # Scanner in = new Scanner(System.in );
    # Int a = in.nextInt();
    # System.out.print(a);}}
    LANGUAGE.JAVA.value: 140,

    # fun main(args: Array<String>){
    # val a:Int = readLine()!!.toInt()
    # print(a)}
    LANGUAGE.KOTLIN.value: 80,

    # #include <iostream>
    # int main(){
    # int a;
    # cin>>a;
    # cout<<a;}
    LANGUAGE.CPP.value: 60
}

LANGUAGE_TO_OUTPUT = {
    LANGUAGE.PYTHON.value: ['print'],
    LANGUAGE.JAVA.value: ['System.out.print'],
    LANGUAGE.KOTLIN.value: ['print'],
    LANGUAGE.CPP.value: ['cout', 'printf']
}

class SPLIT_DICT(Enum):
    INDEX = 'index'
    RATE = 'rate'
    TASKS = 'tasks'


LOGGER_FILE = ROOT_DIR + '../../../../logs.log'
LOGGER_NAME = 'main_logger'

LOGGER_TEST_FILE = ROOT_DIR + '../../../../test_logs.log'

PATH_CMD_ARG = '-path'
ISO_ENCODING = 'ISO-8859-1'
UTF_ENCODING = 'utf8'

ATI_DATA_FOLDER = 'ati_'
DI_DATA_FOLDER = 'di_'
ACTIVITY_TRACKER_FILE_NAME = 'ide-events'

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
MAX_DIF_SEC = 0.5

TEST_DATA_PATH = ROOT_DIR + '/../../resources/test_data'

PREPROCESSING_RESULT_FOLDER = 'preprocessing_result'

# v 2.0 - with stopping after the first break
RUNNING_TESTS_RESULT_FOLDER = 'running_tests_result_2'

MAX_DIFF_SYMBOLS = 30

MAX_SECONDS_TO_WAIT_TEST = 5



