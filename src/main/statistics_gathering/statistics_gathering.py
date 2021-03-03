# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from typing import Any, Set, List

import pandas as pd

from src.main.util import consts
from src.main.util.consts import EXPERIENCE
from src.main.plots.util.consts import STATISTICS_KEY
from src.main.util.log_util import log_and_raise_error
from src.main.processing.task_tracker_handler import handle_tt_file, delete_default_values
from src.main.statistics_gathering.util import Profile, AgeAndExperience, InvalidProfile, InvalidAgeAndExperience, \
    Statistics, InvalidAge, InvalidExperience, StatisticsValue, TaskStatistics
from src.main.util.file_util import get_name_from_path, tt_file_condition, get_output_directory, change_extension_to, \
    serialize_data_and_write_to_file, get_all_file_system_items, contains_substrings_condition, user_subdirs_condition

log = logging.getLogger(consts.LOGGER_NAME)

SUBDIR = consts.FILE_SYSTEM_ITEM.SUBDIR


def is_statistics_key_default_value(value: Any, column: STATISTICS_KEY) -> bool:
    return column.get_default().is_equal(value)


# We must have one value in a profile column otherwise it is an incorrect case
def get_profile_info(tt_df: pd.DataFrame, column: STATISTICS_KEY) -> Profile:
    values = tt_df[column.value].unique()
    values = delete_default_values(values)
    if len(values) == 0:
        # If it's a default value, return consts.DEFAULT_VALUE
        return column.get_default().value
    if len(values) == 1:
        return values[0]
    log_and_raise_error(f'Have found {len(values)}: {values} unique value in profile column {column.value}', log)


def __get_tt_df(tt_file: str, needs_handling: bool = True) -> pd.DataFrame:
    # If we need handling we do it else we read the data
    if needs_handling:
        tt_df, _ = handle_tt_file(tt_file)
        return tt_df
    return pd.read_csv(tt_file, encoding=consts.ISO_ENCODING)


def __get_experience(tt_df: pd.DataFrame) -> Profile:
    if STATISTICS_KEY.EXPERIENCE.value not in tt_df.columns:
        # New data structure
        experience_years = get_profile_info(tt_df, STATISTICS_KEY.EXPERIENCE_YEARS)
        experience_months = get_profile_info(tt_df, STATISTICS_KEY.EXPERIENCE_MONTHS)
        if 0 <= experience_months < 6:
            return EXPERIENCE.LESS_THAN_HALF_YEAR.value
        elif 6 <= experience_months <= 11:
            return EXPERIENCE.FROM_HALF_TO_ONE_YEAR.value
        elif 1 <= experience_years < 2:
            return EXPERIENCE.FROM_ONE_TO_TWO_YEARS.value
        elif 2 <= experience_years < 4:
            return EXPERIENCE.FROM_TWO_TO_FOUR_YEARS.value
        elif 4 <= experience_years < 6:
            return EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value
        elif experience_years >= 6:
            return EXPERIENCE.MORE_THAN_SIX.value
        else:
            return STATISTICS_KEY.EXPERIENCE.get_default()
    return get_profile_info(tt_df, STATISTICS_KEY.EXPERIENCE)


def __get_age_and_experience(tt_file: str, needs_preprocessing: bool = True) -> AgeAndExperience:
    tt_df = __get_tt_df(tt_file, needs_preprocessing)
    age = get_profile_info(tt_df, STATISTICS_KEY.AGE)
    experience = __get_experience(tt_df)
    log.info(f'File: {tt_file}, age is {age}, experience is {experience}')
    return age, experience


# Handle set of profile data values
# Return default_value if files with the same task-tracker id (or the same activity tracker id) have different values
# for profile data (age or experience for example)
# Note: you should run it for each profile column
def __handle_profile_data_of_one_user(profile_data: Set[Profile],
                                      default_value: consts.DEFAULT_VALUE) -> InvalidProfile:
    if default_value in profile_data:
        profile_data.remove(default_value)
    if len(profile_data) == 1:
        return profile_data.pop()
    if consts.INVALID_FILE_FOR_PREPROCESSING in profile_data:
        return consts.INVALID_FILE_FOR_PREPROCESSING
    return default_value


def __get_age_and_experience_of_one_user(ages_and_experiences: List[AgeAndExperience]) -> InvalidAgeAndExperience:
    ages = set([age for age, experience in ages_and_experiences])
    experiences = set([experience for age, experience in ages_and_experiences])
    age = __handle_profile_data_of_one_user(ages, consts.DEFAULT_VALUE.AGE)
    experience = __handle_profile_data_of_one_user(experiences, consts.DEFAULT_VALUE.EXPERIENCE)
    return age, experience


def __get_empty_statistics_dict() -> Statistics:
    return {
        STATISTICS_KEY.AGE: {},
        STATISTICS_KEY.EXPERIENCE: {}
    }


def __update_statistics_dict_column(statistics: Statistics, column: STATISTICS_KEY, value: InvalidProfile) -> None:
    str_value = str(value)
    statistics[column][str_value] = statistics.get(column).get(str_value, 0) + 1


def __add_values_in_statistics_dict(statistics: Statistics, age: InvalidAge, experience: InvalidExperience) -> None:
    __update_statistics_dict_column(statistics, STATISTICS_KEY.AGE, age)
    __update_statistics_dict_column(statistics, STATISTICS_KEY.EXPERIENCE, experience)


def __write_key_result(statistics_value: StatisticsValue, output_directory: str, file_name: str) -> None:
    file_path = os.path.join(output_directory, change_extension_to(file_name, consts.EXTENSION.PICKLE))
    serialize_data_and_write_to_file(file_path, statistics_value)


def __write_results(output_directory: str, statistics: Statistics) -> None:
    for key in statistics.keys():
        __write_key_result(statistics[key], output_directory, key.value)


def get_profile_statistics(path: str) -> str:
    output_directory = get_output_directory(path, consts.STATISTICS_OUTPUT_DIRECTORY)
    folders = get_all_file_system_items(path, user_subdirs_condition, consts.FILE_SYSTEM_ITEM.SUBDIR)
    statistics = __get_empty_statistics_dict()
    for folder in folders:
        log.info(f'Start handling the folder {folder}')
        ct_files = get_all_file_system_items(folder, tt_file_condition)
        age, experience = __get_age_and_experience_of_one_user(list(map(__get_age_and_experience, ct_files)))
        log.info(f'Folder: {folder}, age is {age}, experience is {experience}')
        __add_values_in_statistics_dict(statistics, age, experience)

    __write_results(output_directory, statistics)
    return output_directory


# Run after 'split_tasks_into_separate_files' to return simple statistics dictionary
# Returns how many files we have for each language and task
def get_tasks_statistics(path: str) -> TaskStatistics:
    statistics = {}
    language_values = [language.value for language in consts.LANGUAGE]
    language_folders = get_all_file_system_items(path, contains_substrings_condition(language_values), SUBDIR)
    for l_f in language_folders:
        language = consts.LANGUAGE(get_name_from_path(l_f, False))
        if statistics.get(language):
            log_and_raise_error(f'Duplicate language folder for {language.value}', log)
        statistics[language] = {}
        task_values = consts.TASK.tasks_values()
        task_folders = get_all_file_system_items(l_f, contains_substrings_condition(task_values), SUBDIR)
        for t_f in task_folders:
            files = get_all_file_system_items(t_f)
            task = consts.TASK(get_name_from_path(t_f, False))
            if statistics.get(language).get(task):
                log_and_raise_error(f'Duplicate task for {task.value} in folder {l_f}', log)
            statistics.get(language)[task] = len(files)

    return statistics
