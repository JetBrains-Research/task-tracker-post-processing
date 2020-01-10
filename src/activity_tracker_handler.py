from datetime import datetime
from src import consts
import pandas as pd
import logging
import re

log = logging.getLogger(consts.LOGGER_NAME)


# Filtering the activity-tracker data: returns a new activity-tracker data with deleted not necessary events
# Necessary events can be seen in the const file: ACTIVITY_TRACKER_EVENTS and ACTION_EVENTS
def __filter_ati_data(ati_data: pd.DataFrame):
    event_types = [consts.ACTIVITY_TRACKER_EVENTS.ACTION.value,
                   consts.ACTIVITY_TRACKER_EVENTS.COMPILATION_FINISHED.value]
    ati_data = ati_data[(ati_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value].isin(event_types))
                        & (ati_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value].isin(
        consts.ACTIVITY_TRACKER_EVENTS.action_events()))]
    return ati_data


# Delete : symbol from hours in timestamp for the correct conversion to datetime
# For example 2019-12-09T18:41:28.548+03:00 -> 2019-12-09T18:41:28.548+0300
def __corrected_time(timestamp: str):
    return re.sub(r'([-+]\d{2}):(\d{2})$', r'\1\2', timestamp)


def __get_datetime_by_format(date, datetime_format=consts.DATE_TIME_FORMAT):
    return datetime.strptime(__corrected_time(date), datetime_format)


# Find the closest time to activity tracker time from code tracker time
# if dif between ati_time is more ct_current_time than consts.MAX_DIF_SEC, then the function returns -1
# if ati_time equals ct_current_time, then the function returns 0
# if ati_time equals ct_next_time, then the function returns 1
# In other cases consider differences between ati_time, ct_current_time and ati_time, ct_next_time
# If difference is less or equals consts.MAX_DIF_SEC, then the function returns the index of time, wich has the smallest
# difference (0 for ct_current_time and 1 for ct_next_time)
# In other cases function returns -1
def __get_closest_time(ati_time: datetime, ct_current_time: datetime, ct_next_time: datetime):
    current_dif = (ati_time - ct_current_time).total_seconds()
    # Todo: maybe it can make better???
    if current_dif > consts.MAX_DIF_SEC:
        return -1
    if current_dif == 0:
        return 0
    next_dif = (ct_next_time - ati_time).total_seconds()
    if next_dif == 0:
        return 1
    if current_dif <= consts.MAX_DIF_SEC and next_dif <= consts.MAX_DIF_SEC:
        if current_dif < next_dif:
            return 0
        return 1
    if current_dif <= consts.MAX_DIF_SEC:
        return 0
    if next_dif <= consts.MAX_DIF_SEC:
        return 1
    return -1


def __get_default_dict_for_ati():
    return {
        consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value: [],
        consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value: [],
        consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value: []
    }


# Todo: maybe rename it?
def get_full_default_columns_for_ati(count_rows: int):
    res = __get_default_dict_for_ati()
    for i in range(count_rows):
        __add_values_in_ati_dict(res)
    return res


def __add_values_in_ati_dict(ati_dict: dict, timestamp="", event_type="", event_data=""):
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].append(timestamp)
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value].append(event_type)
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value].append(event_data)


def __add_values_in_ati_dict_by_at_index(res_dict: dict, activity_tracker_data: pd.DataFrame, index: int):
    __add_values_in_ati_dict(res_dict,
                             activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[index],
                             activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value].iloc[index],
                             activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value].iloc[index])


def __is_same_files(code_tracker_file_name: str, activity_tracker_file_path: str):
    activity_tracker_file_name = activity_tracker_file_path.split('/')[-1]
    return code_tracker_file_name == activity_tracker_file_name


# Insert a row to the dataframe before the row_number position.
# For example, we have the dataset with 1 column and 3 rows: A C D
# If we have row_number = 1 and row_value = B, the function returns the dataset with rows: A B C D
def __insert_row(df: pd.DataFrame, row_number: int, row_value: list):
    if row_number > df.index.max() + 1:
        raise ValueError('Invalid row_number in the method __insert_row')
    df1 = df[0:row_number]
    df2 = df[row_number:]
    df1.loc[row_number] = row_value
    df_result = pd.concat([df1, df2])
    df_result.index = [*range(df_result.shape[0])]
    return df_result


# Get an indicator if first_code_tracker_time is included in activity tracker data and a first valid index from
# activity tracker data, which is more or equal than first_code_tracker_time
# Note: return -1, if activity tracker data  does not contain a necessary time and 1 in the other cases
def __get_first_index_for_activity_tracker_data(activity_tracker_data: pd.DataFrame, first_code_tracker_time: datetime,
                                                code_tracker_file_name: str, start_index=0):
    count_other_files = 0
    for index in range(start_index, activity_tracker_data.shape[0]):
        ati_time = __get_datetime_by_format(
            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[index])
        time_dif = (ati_time - first_code_tracker_time).total_seconds()
        activity_tracker_file_path = activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.CURRENT_FILE.value].iloc[
            index]
        if not __is_same_files(activity_tracker_file_path, code_tracker_file_name):
            count_other_files += 1
            continue
        if 0 <= time_dif <= consts.MAX_DIF_SEC:
            return 1, index, count_other_files
        elif time_dif > consts.MAX_DIF_SEC:
            return -1, index, count_other_files
    return -1, activity_tracker_data.shape[0], count_other_files


def __get_ati_index_for_same_file(code_tracker_data: pd.DataFrame, activity_tracker_data: pd.DataFrame,
                                  current_ati_i=0, current_ct_i=0):
    is_same_files = False
    code_tracker_file_name = code_tracker_data[consts.CODE_TRACKER_COLUMN.FILE_NAME.value].iloc[current_ct_i]
    while not is_same_files:
        activity_tracker_file_path = activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.CURRENT_FILE.value].iloc[
            current_ati_i]
        is_same_files = __is_same_files(code_tracker_file_name, activity_tracker_file_path)
        if not is_same_files:
            current_ati_i += 1
        if current_ati_i == activity_tracker_data.shape[0]:
            return current_ati_i
    return current_ati_i


def __handle_missed_ati_elements(activity_tracker_data: pd.DataFrame, code_tracker_data: pd.DataFrame, ct_index: int,
                                 start_ati_index: int, end_ati_index: int, res: dict):
    ct_current_time = __get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[ct_index])
    ct_next_time = __get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[ct_index + 1])
    ct_current_row = list(code_tracker_data.iloc[ct_index])
    ct_next_row = list(code_tracker_data.iloc[ct_index + 1])
    for ati_index in range(start_ati_index, end_ati_index):
        ati_time = __get_datetime_by_format(
            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[ati_index])
        cur_dif = abs((ati_time - ct_current_time).total_seconds())
        next_dif = abs((ati_time - ct_next_time).total_seconds())
        if next_dif < cur_dif:
            code_tracker_data = __insert_row(code_tracker_data, ct_index + 2, ct_next_row)
        else:
            code_tracker_data = __insert_row(code_tracker_data, ct_index + 1, ct_current_row)
        ct_index += 1
        __add_values_in_ati_dict_by_at_index(res, activity_tracker_data, ati_index)
    return code_tracker_data


# Check activity tracker elements and add new rows in code tracker data if activity tracker data has some values which
# are not comparable with timestamps from code tracker data item by the current_ct_i position
def __handle_current_ati_element(code_tracker_data: pd.DataFrame, activity_tracker_data: pd.DataFrame,
                                 current_ct_i: int, current_ati_i: int, res: dict):
    first_code_tracker_time = __get_datetime_by_format(
        code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[current_ct_i])
    code_tracker_file_name = code_tracker_data[consts.CODE_TRACKER_COLUMN.FILE_NAME.value].iloc[current_ct_i]
    is_valid, new_ati_i, count_other_files = __get_first_index_for_activity_tracker_data(activity_tracker_data,
                                                                                         first_code_tracker_time,
                                                                                         code_tracker_file_name,
                                                                                         current_ati_i)

    if new_ati_i - current_ati_i - count_other_files > 1:
        code_tracker_data = __handle_missed_ati_elements(activity_tracker_data, code_tracker_data, current_ct_i,
                                                         current_ati_i, new_ati_i, res)
    return code_tracker_data, new_ati_i, is_valid


# Todo: add tests
def merge_code_tracker_and_activity_tracker_data(code_tracker_data: pd.DataFrame, activity_tracker_data: pd.DataFrame):
    log.info('...starting to filter activity tracker data')
    activity_tracker_data = __filter_ati_data(activity_tracker_data)
    log.info('finish to filter activity tracker data')
    res = __get_default_dict_for_ati()

    # Miss other files
    ati_i = __get_ati_index_for_same_file(code_tracker_data, activity_tracker_data)
    code_tracker_data_size = code_tracker_data.shape[0]
    for ct_i in range(0, code_tracker_data_size - 1):
        code_tracker_data, ati_i, is_valid = __handle_current_ati_element(code_tracker_data, activity_tracker_data,
                                                                          ct_i, ati_i, res)

        if is_valid == -1 or ati_i >= activity_tracker_data.shape[0]:
            __add_values_in_ati_dict(res)
            continue

        ati_time = __get_datetime_by_format(
            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[ati_i])
        ct_current_time = __get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[ct_i])
        ct_next_time = __get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[ct_i + 1])
        closest_time = __get_closest_time(ati_time, ct_current_time, ct_next_time)
        if closest_time == 0:
            __add_values_in_ati_dict_by_at_index(res, activity_tracker_data, ati_i)
            ati_i += 1
        else:
            __add_values_in_ati_dict(res)

    # handle the last element from code tracker data
    if ati_i < activity_tracker_data.shape[0]:
        code_tracker_data, ati_i, is_valid = __handle_current_ati_element(code_tracker_data, activity_tracker_data,
                                                                          code_tracker_data_size - 1, ati_i, res)

        if is_valid != -1:
            __add_values_in_ati_dict_by_at_index(res, activity_tracker_data, ati_i)
        else:
            __add_values_in_ati_dict(res)
    else:
        __add_values_in_ati_dict(res)

    log.info('finish getting activity tracker info')
    return code_tracker_data, res
