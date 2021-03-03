# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pandas as pd

from src.main.plots.util.consts import STATISTICS_KEY
from src.main.statistics_gathering.statistics_gathering import get_profile_info
from src.main.util import consts
from src.main.util.consts import FILE_SYSTEM_ITEM
from src.main.util.data_util import handle_folder
from src.main.util.file_util import get_all_file_system_items, language_item_condition, get_output_directory

EXPERIENCE = consts.TASK_TRACKER_COLUMN.EXPERIENCE.value
EXPERIENCE_YEARS = consts.TASK_TRACKER_COLUMN.EXPERIENCE_YEARS.value
EXPERIENCE_MONTHS = consts.TASK_TRACKER_COLUMN.EXPERIENCE_MONTHS.value


def __unify_program_experience(df: pd.DataFrame) -> pd.DataFrame:
    if EXPERIENCE_YEARS and EXPERIENCE_MONTHS in df.columns:
        experience_years = get_profile_info(df, STATISTICS_KEY.EXPERIENCE_YEARS)
        experience_months = get_profile_info(df, STATISTICS_KEY.EXPERIENCE_MONTHS)
        if 0 <= experience_months < 6:
            df[EXPERIENCE] = consts.EXPERIENCE.LESS_THAN_HALF_YEAR.value
        elif 6 <= experience_months <= 11:
            df[EXPERIENCE] = consts.EXPERIENCE.FROM_HALF_TO_ONE_YEAR.value
        elif 1 <= experience_years < 2:
            df[EXPERIENCE] = consts.EXPERIENCE.FROM_ONE_TO_TWO_YEARS.value
        elif 2 <= experience_years < 4:
            df[EXPERIENCE] = consts.EXPERIENCE.FROM_TWO_TO_FOUR_YEARS.value
        elif 4 <= experience_years < 6:
            df[EXPERIENCE] = consts.EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value
        elif experience_years >= 6:
            df[EXPERIENCE] = consts.EXPERIENCE.MORE_THAN_SIX.value
        else:
            df[EXPERIENCE] = None

        del df[EXPERIENCE_YEARS]
        del df[EXPERIENCE_MONTHS]

    return df


def unify_program_experience(path: str, output_directory_prefix: str = 'unify_program_experience') -> str:
    """
    This function allows to unify program experience:

    new data contains two columns: programExperienceYears and programExperienceMonths
    this function allows to categorize them (see enum class EXPERIENCE):

    LESS_THAN_HALF_YEAR = 'LESS_THAN_HALF_YEAR'
    FROM_HALF_TO_ONE_YEAR = 'FROM_HALF_TO_ONE_YEAR'
    FROM_ONE_TO_TWO_YEARS = 'FROM_ONE_TO_TWO_YEARS'
    FROM_TWO_TO_FOUR_YEARS = 'FROM_TWO_TO_FOUR_YEARS'
    FROM_FOUR_TO_SIX_YEARS = 'FROM_FOUR_TO_SIX_YEARS'
    MORE_THAN_SIX = 'MORE_THAN_SIX'

    After executing the function, the dataset will have only EXPERIENCE column
    (EXPERIENCE_YEARS and EXPERIENCE_MONTHS will be deleted)
    """
    languages = get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
    output_directory = get_output_directory(path, output_directory_prefix)
    for _ in languages:
        handle_folder(path, output_directory_prefix, __unify_program_experience)
    return output_directory
