# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from enum import Enum
from typing import List, Dict

import plotly.express as px

from src.main.util.consts import TASK, TASK_STATUS, DEFAULT_VALUE, CODE_TRACKER_COLUMN, RESOURCES_PATH


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

    @classmethod
    def get_events(cls) -> List['ATI_RUN_EVENT']:
        return [e for e in ATI_RUN_EVENT]


ATI_RUN_EVENT_COLOR_DICT: Dict[ATI_RUN_EVENT, str] = {
    ATI_RUN_EVENT.RUN: '#2EA031',
    ATI_RUN_EVENT.RERUN: '#2EB167',
    ATI_RUN_EVENT.RUN_CLASS: '#B0DF8C',
    ATI_RUN_EVENT.DEBUG_CLASS: '#A7CEE3',
    ATI_RUN_EVENT.DEBUG: '#A7CEE3',
    ATI_RUN_EVENT.STOP: '#E31C19',
    ATI_RUN_EVENT.RESUME: '#FE7F05',
    ATI_RUN_EVENT.STEP_INTO: '#FCBF70',
    ATI_RUN_EVENT.COMPILE_DIRTY: '#FB9A99'
}


class ATI_EDITOR_EVENT(Enum):
    EDITOR_COPY = 'EditorCopy'
    COPY = '$Copy'
    EDITOR_PASTE = 'EditorPaste'
    PASTE = '$Paste'
    EDITOR_CUT = 'EditorCut'
    REFORMAT_CODE = 'ReformatCode'
    UNDO = '$Undo'

    @classmethod
    def get_events(cls) -> List['ATI_EDITOR_EVENT']:
        return [e for e in ATI_EDITOR_EVENT]


ATI_EDITOR_EVENT_COLOR_DICT: Dict[ATI_EDITOR_EVENT, str] = {
    ATI_EDITOR_EVENT.EDITOR_COPY: '#2EA031',
    ATI_EDITOR_EVENT.COPY: '#B0DF8C',
    ATI_EDITOR_EVENT.EDITOR_PASTE: '#2778B3',
    ATI_EDITOR_EVENT.PASTE: '#A7CEE3',
    ATI_EDITOR_EVENT.EDITOR_CUT: '#6C3D99',
    ATI_EDITOR_EVENT.REFORMAT_CODE: '#FE7F05',
    ATI_EDITOR_EVENT.UNDO: '#E31C19'
}

TASK_COLOR_DICT: Dict[TASK, str] = {
    TASK.PIES: '#B8C4DD',
    TASK.MAX_3: '#FFF3CC',
    TASK.VOTING: '#F9D4CE',
    TASK.ZERO: '#D5F5F5',
    TASK.MAX_DIGIT: '#E9DFEF',
    TASK.BRACKETS: '#DAE3D9'
}


BAR_PALETTE = px.colors.sequential.Sunset


TASK_STATUS_COLOR_DICT: Dict[TASK_STATUS, str] = {
    TASK_STATUS.SOLVED: '#65C32A',
    TASK_STATUS.NOT_SOLVED: '#D16B48'
}

FRAGMENT_LENGTH_COL = 'fragment_length'

FRAGMENT_LENGTH_COLOR = '#737DBB'

SHORT_NAME_LENGTH = 10

SMALL_SIZE = 2
LARGE_SIZE = 50


class STATISTICS_KEY(Enum):
    AGE = CODE_TRACKER_COLUMN.AGE.value
    EXPERIENCE = CODE_TRACKER_COLUMN.EXPERIENCE.value
    NODES_NUMBER = 'Nodes number'

    def get_default(self) -> DEFAULT_VALUE:
        if self == STATISTICS_KEY.AGE:
            return DEFAULT_VALUE.AGE
        elif self == STATISTICS_KEY.EXPERIENCE:
            return DEFAULT_VALUE.EXPERIENCE


STATISTICS_FREQ = 'freq'
STATISTICS_PERCENTS = 'percents'


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


class CHART_TYPE(Enum):
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
    TRACE = 'trace'


DEFAULT_PATH_FOR_PLOTS = os.path.join(RESOURCES_PATH, 'plots')
