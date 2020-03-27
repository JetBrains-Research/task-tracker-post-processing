from typing import Union, Tuple, Dict

from src.main.plots.util.consts import STATISTICS_KEY
from src.main.util import consts

Age = Union[int, consts.DEFAULT_VALUE]
Experience = Union[str, consts.DEFAULT_VALUE]
AgeAndExperience = Tuple[Age, Experience]
Profile = Union[Age, Experience]

# If file is invalid then consts.INVALID_FILE_FOR_PREPROCESSING is returned with type int
InvalidAge = Union[int, Age]
InvalidExperience = Union[int, Experience]
InvalidAgeAndExperience = Tuple[InvalidAge, InvalidExperience]
InvalidProfile = Union[int, Age, Experience]

# For each STATISTIC_KEY we gather which values (casted to str) and how many we have
StatisticsValue = Dict[str, int]
Statistics = Dict[STATISTICS_KEY, StatisticsValue]

# For each LANGUAGE and TASK we gather how many files we have
TaskStatistics = Dict[consts.LANGUAGE, Dict[consts.TASK, int]]
