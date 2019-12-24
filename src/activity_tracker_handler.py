from datetime import datetime
from src import consts
import pandas as pd
import logging
import re

log = logging.getLogger(consts.LOGGER_NAME)


# Delete not necessary events from activity-tracker data
# Necessary events can see in the const file: ACTIVITY_TRACKER_EVENTS and ACTION_EVENTS
def __filter_ati_data(ati_data: pd.DataFrame):
    event_types = [consts.ACTIVITY_TRACKER_EVENTS.ACTION.value,
                   consts.ACTIVITY_TRACKER_EVENTS.COMPILATION_FINISHED.value]
    ati_data = ati_data[(ati_data[consts.COLUMN.EVENT_TYPE.value].isin(event_types))
                        & (ati_data[consts.COLUMN.EVENT_DATA.value].isin(consts.ACTION_EVENTS))]
    return ati_data


# Delete : symbol from hours in timestamp for correcting convert to datetime
# For example 2019-12-09T18:41:28.548+03:00 -> 2019-12-09T18:41:28.548+0300
def __corrected_time(timestamp: str):
    return re.sub(r'([-+]\d{2}):(\d{2})(?:(\d{2}))?$', r'\1\2\3', timestamp)


# Find the closest time to activity tracker time from code tracker time
# if dif between ati_time more ct_current_time then consts.MAX_DIF_SEC, then the function return -1
# if ati_time equals ct_current_time, then the function return 0
# if ati_time equals ct_next_time, then the function return 1
# In other cases consider differences between ati_time, ct_current_time and ati_time, ct_next_time
# If difference less or equals consts.MAX_DIF_SEC, then the function return a index of time, witch has smallest
# difference (0 for ct_current_time and 1 for ct_next_time)
# In other cases function return -1
def __get_closest_time(ati_time: datetime, ct_current_time: datetime, ct_next_time: datetime):
    current_dif = (ati_time - ct_current_time).total_seconds()
    # Todo: maybe it can make better???
    # Todo: add comparing for files names???
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


def __add_empty_value(dic: dict, empty_value=''):
    for key in dic.keys():
        dic[key].append(empty_value)


def __get_default_dict_for_ati():
    return {
        consts.COLUMN.TIMESTAMP_ATI.value: [],
        consts.COLUMN.EVENT_TYPE.value: [],
        consts.COLUMN.EVENT_DATA.value: []
    }


# Todo: maybe rename it?
def get_full_default_columns_for_ati(count_rows: int):
    res = __get_default_dict_for_ati()
    for i in range(count_rows):
        __add_empty_value(res)
    return res


def __add_values_in_ati_dict(ati_dict: dict, timestamp: str,  event_type: str, event_data: str):
    ati_dict[consts.COLUMN.TIMESTAMP_ATI.value].append(timestamp)
    ati_dict[consts.COLUMN.EVENT_TYPE.value].append(event_type)
    ati_dict[consts.COLUMN.EVENT_DATA.value].append(event_data)


def __get_datetime_by_format(date, datetime_format=consts.DATE_TIME_FORMAT):
    return datetime.strptime(__corrected_time(date), datetime_format)


# Get a first valid index from activity tracker data, which is more or equal then first_code_tracker_time
def __get_first_index_for_activity_tracker_data(activity_tracker_data: pd.DataFrame, first_code_tracker_time: datetime,
                                                start_index=0):
    for index in range(start_index, activity_tracker_data.shape[0]):
        ati_time = __get_datetime_by_format(activity_tracker_data[consts.COLUMN.TIMESTAMP_ATI.value].iloc[index])
        time_dif = (ati_time - first_code_tracker_time).total_seconds()
        if 0 <= time_dif <= consts.MAX_DIF_SEC:
            return index
    return -1


def merge_code_tracker_and_activity_tracker_data(code_tracker_data: pd.DataFrame, activity_tracker_data: pd.DataFrame):
    log.info('...starting to filter activity tracker data')
    activity_tracker_data = __filter_ati_data(activity_tracker_data)
    log.info('finish to filter activity tracker data')
    res = __get_default_dict_for_ati()

    ati_i = 0
    code_tracker_data_size = code_tracker_data.shape[0]
    for ct_i in range(0, code_tracker_data_size - 1):
        ati_i = __get_first_index_for_activity_tracker_data(activity_tracker_data, __get_datetime_by_format(
            code_tracker_data[consts.COLUMN.DATE.value].iloc[ct_i]), ati_i)
        if ati_i == -1 or ati_i >= activity_tracker_data.shape[0]:
            __add_empty_value(res)
            continue

        ati_time = __get_datetime_by_format(activity_tracker_data[consts.COLUMN.TIMESTAMP_ATI.value].iloc[ati_i])
        ct_current_time = __get_datetime_by_format(code_tracker_data[consts.COLUMN.DATE.value].iloc[ct_i])
        ct_next_time = __get_datetime_by_format(code_tracker_data[consts.COLUMN.DATE.value].iloc[ct_i + 1])
        closest_time = __get_closest_time(ati_time, ct_current_time, ct_next_time)
        if closest_time == 0:
            __add_values_in_ati_dict(res, activity_tracker_data[consts.COLUMN.TIMESTAMP_ATI.value].iloc[ati_i],
                                     activity_tracker_data[consts.COLUMN.EVENT_TYPE.value].iloc[ati_i],
                                     activity_tracker_data[consts.COLUMN.EVENT_DATA.value].iloc[ati_i])
            ati_i += 1
        else:
            __add_empty_value(res)

    # handle the last element from code tracker data
    if ati_i != -1 and ati_i < activity_tracker_data.shape[0]:
        ati_i = __get_first_index_for_activity_tracker_data(activity_tracker_data,
                                                            code_tracker_data[consts.COLUMN.DATE.value].iloc[
                                                              code_tracker_data_size - 1], ati_i)
        if ati_i != -1:
            __add_values_in_ati_dict(res, activity_tracker_data[consts.COLUMN.TIMESTAMP_ATI.value].iloc[ati_i],
                                     activity_tracker_data[consts.COLUMN.EVENT_TYPE.value].iloc[ati_i],
                                     activity_tracker_data[consts.COLUMN.EVENT_DATA.value].iloc[ati_i])
        else:
            __add_empty_value(res)
    else:
        __add_empty_value(res)

    log.info('finish getting activity tracker info')
    return res
