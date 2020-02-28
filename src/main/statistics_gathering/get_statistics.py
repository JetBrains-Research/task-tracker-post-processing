import logging
import os
import pandas as pd

from src.main.util import consts
from src.main.plots import consts as stat_const
from src.main.util.file_util import get_all_file_system_items, data_subdirs_condition, csv_file_condition, \
    get_result_folder, create_file, change_extension_to
from src.main.preprocessing.preprocessing import __separate_ati_and_other_files
from src.main.preprocessing.code_tracker_handler import handle_ct_file


log = logging.getLogger(consts.LOGGER_NAME)


# We must have one value in a profile column else it is an incorrect case
def __get_profile_info(ct_df: pd.DataFrame, column: consts.CODE_TRACKER_COLUMN):
    values = ct_df[column].unique()
    if len(values) == 1:
        return values[0]
    log.error(f'Have found {len(values)} unique value in profile column {column}')
    raise ValueError(f'Have found {len(values)} unique value in profile column {column}')


def __get_ct_df(ct_file: str, needs_preprocessing=True):
    # If we need preprocessing we do it else we read the data
    if needs_preprocessing:
        ct_df, _ = handle_ct_file(ct_file)
        return ct_df
    return pd.read_csv(ct_file, encoding=consts.ISO_ENCODING)


def __get_age_and_experience(ct_file: str, needs_preprocessing=True):
    ct_df = __get_ct_df(ct_file, needs_preprocessing)
    age = __get_profile_info(ct_df, consts.CODE_TRACKER_COLUMN.AGE.value)
    experience = __get_profile_info(ct_df, consts.CODE_TRACKER_COLUMN.EXPERIENCE.value)
    log.info(f'File: {ct_file}, age is {age}, experience is {experience}')
    return age, experience


# Handle set of profile data values
# Return default_value if files with the same code tracker id (or the same activity tracker id) have differents values
# for profile data (age or experience for example)
# Note: you should run it for each profile column
def __handle_profile_data_of_one_student(profile_data: set, default_value=None):
    if len(profile_data) == 1:
        return profile_data.pop()
    return default_value


def __get_age_and_experience_by_one_user(ages_and_experiences: list):
    ages = set([pair[0] for pair in ages_and_experiences])
    experiences = set([pair[1] for pair in ages_and_experiences])
    age = __handle_profile_data_of_one_student(ages, consts.DEFAULT_VALUES.AGE.value)
    experience = __handle_profile_data_of_one_student(experiences, consts.DEFAULT_VALUES.EXPERIENCE.value)
    return age, experience


def __get_empty_statistics_dict():
    return {
        stat_const.STATISTICS_COLUMN.AGE.value: {},
        stat_const.STATISTICS_COLUMN.EXPERIENCE.value: {}
    }


def __update_statistics_dict_column(statistics: dict, column: stat_const.STATISTICS_COLUMN, value=None):
    str_value = str(value)
    if statistics.get(column).get(str_value) is None:
        statistics[column][str_value] = 1
    else:
        statistics[column][str_value] += 1


def __add_values_in_statistics_dict(statistics: dict, age: int, experience: str):
    __update_statistics_dict_column(statistics, stat_const.STATISTICS_COLUMN.AGE.value, age)
    __update_statistics_dict_column(statistics, stat_const.STATISTICS_COLUMN.EXPERIENCE.value, experience)


# Get content for writing in the file in the format: key value
def __get_result_content(statistics_value: dict):
    content = ''
    for key, value in statistics_value.items():
        content += str(key) + ' ' + str(value) + '\n'
    return content


def __write_key_result(statistics_value: dict, result_folder: str, file_name: str):
    file_path = os.path.join(result_folder, change_extension_to(file_name, 'txt'))
    create_file(__get_result_content(statistics_value), file_path)


def __write_results(result_folder: str, statistics: dict):
    __write_key_result(statistics[stat_const.STATISTICS_COLUMN.AGE.value], result_folder,
                       stat_const.STATISTICS_COLUMN.AGE.value)
    __write_key_result(statistics[stat_const.STATISTICS_COLUMN.EXPERIENCE.value], result_folder,
                       stat_const.STATISTICS_COLUMN.EXPERIENCE.value)


# Todo: it is the same with the method preprocess_data from preprocessing.py. Maybe to make a general method?
def get_statistics(path: str):
    result_folder = get_result_folder(path, consts.STATISTICS_RESULT_FOLDER)
    folders = get_all_file_system_items(path, data_subdirs_condition, consts.FILE_SYSTEM_ITEM.SUBDIR.value)
    statistics = __get_empty_statistics_dict()
    for folder in folders:
        log.info(f'Start handling the folder {folder}')
        files = get_all_file_system_items(folder, csv_file_condition, consts.FILE_SYSTEM_ITEM.FILE.value)
        try:
            ct_files, _ = __separate_ati_and_other_files(files)
            age, experience = __get_age_and_experience_by_one_user(list(map(__get_age_and_experience, ct_files)))
            log.info(f'Folder: {folder}, age is {age}, experience is {experience}')
            __add_values_in_statistics_dict(statistics, age, experience)
        # Drop the current folder
        except ValueError:
            continue

    __write_results(result_folder, statistics)

