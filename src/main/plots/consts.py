from enum import Enum

import plotly.express as px

from src.main.util.consts import TASK, TASK_STATUS


class ATI_RUN_EVENT(Enum):
    RUN = 'Run'
    RERUN = 'Rerun'
    RUN_CLASS = 'RunClass'
    DEBUG_CLASS = 'DebugClass'
    DEBUG = 'Debug'
    STOP = 'Stop'
    RESUME = 'Resume'
    STEP_INTO = 'StepInto'
    COMPILE_DIRTY = 'CompileDirty'


ATI_RUN_EVENT_COLOR_DICT = {
    ATI_RUN_EVENT.RUN.value: '#2EA031',
    ATI_RUN_EVENT.RERUN.value: '#2EB167',
    ATI_RUN_EVENT.RUN_CLASS.value: '#B0DF8C',
    ATI_RUN_EVENT.DEBUG_CLASS.value: '#A7CEE3',
    ATI_RUN_EVENT.DEBUG.value: '#A7CEE3',
    ATI_RUN_EVENT.STOP.value: '#E31C19',
    ATI_RUN_EVENT.RESUME.value: '#FE7F05',
    ATI_RUN_EVENT.STEP_INTO.value: '#FCBF70',
    ATI_RUN_EVENT.COMPILE_DIRTY.value: '#FB9A99'
}


class ATI_EDITOR_EVENT(Enum):
    EDITOR_COPY = 'EditorCopy'
    COPY = '$Copy'
    EDITOR_PASTE = 'EditorPaste'
    PASTE = '$Paste'
    EDITOR_CUT = 'EditorCut'
    REFORMAT_CODE = 'ReformatCode'
    UNDO = '$Undo'


ATI_EDITOR_EVENT_COLOR_DICT = {
    ATI_EDITOR_EVENT.EDITOR_COPY.value: '#2EA031',
    ATI_EDITOR_EVENT.COPY.value: '#B0DF8C',
    ATI_EDITOR_EVENT.EDITOR_PASTE.value: '#2778B3',
    ATI_EDITOR_EVENT.PASTE.value: '#A7CEE3',
    ATI_EDITOR_EVENT.EDITOR_CUT.value: '#6C3D99',
    ATI_EDITOR_EVENT.REFORMAT_CODE.value: '#FE7F05',
    ATI_EDITOR_EVENT.UNDO.value: '#E31C19'
}

TASK_COLOR_DICT = {
    TASK.PIES.value: '#B8C4DD',
    TASK.MAX_3.value: '#FFF3CC',
    TASK.ELECTION.value: '#F9D4CE',
    TASK.ZERO.value: '#D5F5F5',
    TASK.MAX_DIGIT.value: '#E9DFEF',
    TASK.BRACKETS.value: '#DAE3D9'
}


BAR_PALETTE = px.colors.sequential.Sunset


TASK_STATUS_COLOR_DICT = {
    TASK_STATUS.SOLVED.value: '#65C32A',
    TASK_STATUS.NOT_SOLVED.value: '#D16B48'
}

FRAGMENT_LENGTH_COL = 'fragment_length'
FRAGMENT_LENGTH_COLOR = '#737DBB'

SHORT_NAME_LENGTH = 10

SMALL_SIZE = 2
LARGE_SIZE = 50


class STATISTICS_KEY(Enum):
    AGE = 'age'
    EXPERIENCE = 'experience'

    @classmethod
    def statistics_keys(cls):
        return [cls.AGE.value, cls.EXPERIENCE.value]


STATISTIC_FREQ = 'freq'


class STATISTICS_SHOWING_KEY(Enum):
    INCORRECT = 'Incorrect value'
    NOT_INDICATED = 'Not indicated'
    OTHERS = 'Others',
    FREQ = 'Frequency'


STATISTICS_RARE_VALUE_THRESHOLD = 2


class STATISTICS_COLORS(Enum):
    PIE_CHART = px.colors.sequential.Sunset
    BAR_CHART_BG = '#FFFAE3'
    BAR_CHART_COLS = '#9B0B9B'


DEFAULT_BAR_CHART_COLOR = '#9B0B9B'


class PLOT_TYPES(Enum):
    PIE = 'pie'
    BAR = 'bar'


class STATISTICS_INFO_FOR_PLOTS(Enum):
    LABELS = 'labels'
    TITLE = 'title'


# 'total ascending' means: in order of increasing values in Y
# 'category ascending' means: in order of increasing values in X
class PLOTTY_CATEGORY_ORDER(Enum):
    TOTAL_ASCENDING = 'total ascending'
    CATEGORY_ASCENDING = 'category ascending'
