from enum import Enum
import plotly.express as px

STATUS_COLOR_SIZE_DICT = {
    'SOLVED': ['go', 5],
    'NOT_SOLVED': ['ro', 5],
}

STATUS_COLOR_SIZE_DEFAULT = ['bo', 1]

TASK_COLOR_DICT = {
    'pies': 'ro',
    'max3': 'yo',
    'election': 'go',
    'isZero': 'co',
    'maxDigit': 'bo',
    'brackets': 'mo'
}

TASK_COLOR_DEFAULT = 'ko'
DATA_ROOT_ARG = '-root'

TASK_SPLITTING_ROWS_DELTA = 10
TASK_SPLITTING_DIFFS_DELTA = 30
SHORT_NAME_LENGTH = 10
DIFF_MAX = 30


class STATISTIC_KEY(Enum):
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


class PLOT_TYPES(Enum):
    PIE = 'pie'
    BAR = 'bar'


class STATISTICS_INFO_FOR_PLOTS(Enum):
    LABELS = 'labels'
    TITLE = 'title'


class OUTPUT_FORMAT(Enum):
    HTML = '.html'


# 'total ascending' means: in order of increasing values in Y
# 'category ascending' means: in order of increasing values in X
class PLOTTY_CATEGORY_ORDER(Enum):
    TOTAL_ASCENDING = 'total ascending'
    CATEGORY_ASCENDING = 'category ascending'



