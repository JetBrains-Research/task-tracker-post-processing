from datetime import datetime
from src import consts
import pandas as pd
import logging
import re

log = logging.getLogger(consts.LOGGER_NAME)


# Unification of similar activity tracker events. For example, an action Run by pressed the button Run and by
# pressing a combination of buttons is not similar in the source data. After the unification, the function returns a
# new activity tracker data with the union this kind of events
def __unification_of_activity_tracker_columns(ati_data: pd.DataFrame):
    action_events = consts.ACTIVITY_TRACKER_EVENTS.action_events()
    for index in range(ati_data.shape[0]):
        current_focused_component = ati_data[consts.ACTIVITY_TRACKER_COLUMN.FOCUSED_COMPONENT.value].iloc[index]
        if current_focused_component in action_events:
            # Todo: rewrite with __setitem__ ??
            ati_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value].iloc[index] \
                = ati_data[consts.ACTIVITY_TRACKER_COLUMN.FOCUSED_COMPONENT.value].iloc[index]
            ati_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value].iloc[index] \
                = consts.ACTIVITY_TRACKER_EVENTS.ACTION.value
    return ati_data


# Filtering the activity-tracker data: returns a new activity-tracker data with deleted not necessary events
# Necessary events can be seen in the const file: ACTIVITY_TRACKER_EVENTS and ACTION_EVENTS
def __filter_ati_data(ati_data: pd.DataFrame):
    event_types = [consts.ACTIVITY_TRACKER_EVENTS.ACTION.value,
                   consts.ACTIVITY_TRACKER_EVENTS.COMPILATION_FINISHED.value]
    action_events = consts.ACTIVITY_TRACKER_EVENTS.action_events()
    ati_data = ati_data[(ati_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value].isin(event_types))
                        & (ati_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value].isin(action_events))]
    ati_data.index = [*range(ati_data.shape[0])]
    return ati_data


# Delete : symbol from hours in timestamp for the correct conversion to datetime
# For example 2019-12-09T18:41:28.548+03:00 -> 2019-12-09T18:41:28.548+0300
def __corrected_time(timestamp: str):
    return re.sub(r'([-+]\d{2}):(\d{2})$', r'\1\2', timestamp)


def __get_datetime_by_format(date, datetime_format=consts.DATE_TIME_FORMAT):
    return datetime.strptime(__corrected_time(date), datetime_format)


# Find the closest time to activity tracker time from code tracker time
# The function returns 0 if the current code tracker time is the closest time
# The function returns 1 if the next code tracker time is the closest time
# The function returns 2 if the current code tracker time is not the closest time, but the next code tracker time
# is more than the activity tracker time
# In other cases function returns -1
def __get_closest_time(ati_time: datetime, ct_current_time: datetime, ct_next_time: datetime):
    current_dif = (ati_time - ct_current_time).total_seconds()
    # Todo: maybe it can make better???
    if current_dif == 0:
        return 0
    next_dif = (ct_next_time - ati_time).total_seconds()
    if next_dif == 0:
        return 1
    if current_dif <= consts.MAX_DIF_SEC and 0 <= next_dif <= consts.MAX_DIF_SEC:
        if current_dif < next_dif:
            return 0
        return 1
    if current_dif <= consts.MAX_DIF_SEC:
        return 0
    if 0 <= next_dif <= consts.MAX_DIF_SEC:
        return 1
    if current_dif > consts.MAX_DIF_SEC and next_dif >= 0:
        return 2
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
    if pd.isnull(activity_tracker_file_path):
        return False
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
    # Todo: maybe create a new data frame and join?
    df1.loc[row_number] = row_value
    df_result = pd.concat([df1, df2])
    df_result.index = [*range(df_result.shape[0])]
    return df_result


# Get an indicator if first_code_tracker_time is included in activity tracker data and a first valid index from
# activity tracker data, which is more or equal than first_code_tracker_time
# Note: return -1, if activity tracker data  does not contain a necessary time and 1 in the other cases
def __get_first_index_for_activity_tracker_data(activity_tracker_data: pd.DataFrame, first_code_tracker_time: datetime,
                                                code_tracker_file_name: str, start_index=0):
    other_files = []
    for index in range(start_index, activity_tracker_data.shape[0]):
        ati_time = __get_datetime_by_format(
            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[index])
        time_dif = (ati_time - first_code_tracker_time).total_seconds()
        activity_tracker_file_path = activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.CURRENT_FILE.value].iloc[
            index]
        if not __is_same_files(code_tracker_file_name, activity_tracker_file_path):
            other_files.append(index)
            continue
        if 0 <= time_dif <= consts.MAX_DIF_SEC:
            return 1, index, other_files
        elif time_dif > consts.MAX_DIF_SEC:
            return 1, index, other_files
    return -1, activity_tracker_data.shape[0], other_files


def __get_ati_index_for_same_file(code_tracker_data: pd.DataFrame, activity_tracker_data: pd.DataFrame,
                                  current_ati_i=0, current_ct_i=0):
    is_same_files = False
    code_tracker_file_name = code_tracker_data[consts.CODE_TRACKER_COLUMN.FILE_NAME.value].iloc[current_ct_i]
    while not is_same_files:
        activity_tracker_file_path = activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.CURRENT_FILE.value].iloc[
            current_ati_i]
        is_same_files = __is_same_files(code_tracker_file_name, activity_tracker_file_path)
        if is_same_files:
            return current_ati_i
        if current_ati_i == activity_tracker_data.shape[0] - 1:
            return current_ati_i
        current_ati_i += 1
    return current_ati_i


def __handle_missed_ati_elements(activity_tracker_data: pd.DataFrame, code_tracker_data: pd.DataFrame, ct_index: int,
                                 start_ati_index: int, end_ati_index: int, res: dict, other_files: list):
    ct_current_time = __get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[ct_index])
    ct_current_row = list(code_tracker_data.iloc[ct_index])
    if ct_index == code_tracker_data.shape[0] - 1:
        ct_next_time = ct_current_time
        ct_next_row = ct_current_row
    else:
        ct_next_time = __get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[ct_index + 1])
        ct_next_row = list(code_tracker_data.iloc[ct_index + 1])
    for ati_index in range(start_ati_index, end_ati_index):
        if ati_index in other_files:
            continue
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
    is_valid, new_ati_i, other_files = __get_first_index_for_activity_tracker_data(activity_tracker_data,
                                                                                   first_code_tracker_time,
                                                                                   code_tracker_file_name,
                                                                                   current_ati_i)

    if new_ati_i - current_ati_i > 1:
        code_tracker_data = __handle_missed_ati_elements(activity_tracker_data, code_tracker_data, current_ct_i,
                                                         current_ati_i, new_ati_i, res, other_files)
    return code_tracker_data, new_ati_i, is_valid


# The function handles the closest time result
# If the closest time result is 0, then the current code tracker time is valid for the current activity tracker data
# and we should add the activity tracker value to the current code tracker row and give a next activity tracker element
# If the closest time result is 1, then the next code tracker time is valid and we should miss the current code tracker
# item
# If the closest time result is 2, then we should duplicate the current code tracker row and union it with the current
# activity tracker row
# In the other cases we should miss the current code tracker item because the next code tracker time is valid
def __handle_closest_time_result(closest_time_res: int, ati_i: int, ct_i: int, activity_tracker_data: pd.DataFrame,
                                 code_tracker_data: pd.DataFrame, res: dict):
    if closest_time_res != 0 and closest_time_res != 2:
        __add_values_in_ati_dict(res)
        ct_i += 1
    if closest_time_res == 0:
        __add_values_in_ati_dict_by_at_index(res, activity_tracker_data, ati_i)
        ati_i += 1
    elif closest_time_res == 2:
        code_tracker_data = __handle_missed_ati_elements(activity_tracker_data, code_tracker_data, ct_i, ati_i,
                                                         ati_i + 1, res, [])
        ati_i += 1
    return ati_i, ct_i, code_tracker_data


# Get size of result for activity tracker data
def __get_dict_lists_size(res: dict):
    size = 0
    for key in res.keys():
        if size != 0 and len(res[key]) != size:
            raise ValueError('Lists in the res dict have different sizes')
        size = len(res[key])
    return size


def merge_code_tracker_and_activity_tracker_data(code_tracker_data: pd.DataFrame, activity_tracker_data: pd.DataFrame):
    log.info('...starting to unificate activity tracker data')
    activity_tracker_data = __unification_of_activity_tracker_columns(activity_tracker_data)
    log.info('finish to unificate activity tracker data')

    log.info('...starting to filter activity tracker data')
    activity_tracker_data = __filter_ati_data(activity_tracker_data)
    log.info('finish to filter activity tracker data')
    res = __get_default_dict_for_ati()

    # Miss other files
    ati_i = __get_ati_index_for_same_file(code_tracker_data, activity_tracker_data)
    code_tracker_data_size = code_tracker_data.shape[0]
    ct_i = 0
    while ct_i < code_tracker_data_size - 1:
        code_tracker_data, ati_i, is_valid = __handle_current_ati_element(code_tracker_data, activity_tracker_data,
                                                                          ct_i, ati_i, res)

        if code_tracker_data.shape[0] > code_tracker_data_size:
            ct_i += code_tracker_data.shape[0] - code_tracker_data_size
            code_tracker_data_size = code_tracker_data.shape[0]

        if is_valid == -1 or ati_i >= activity_tracker_data.shape[0]:
            __add_values_in_ati_dict(res)
            ct_i += 1
            continue

        ati_time = __get_datetime_by_format(
            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[ati_i])
        ct_current_time = __get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[ct_i])
        ct_next_time = __get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[ct_i + 1])
        closest_time = __get_closest_time(ati_time, ct_current_time, ct_next_time)

        ati_i, ct_i, code_tracker_data = __handle_closest_time_result(closest_time, ati_i, ct_i, activity_tracker_data,
                                                                      code_tracker_data, res)

    # handle the last element from the code tracker data
    while ati_i < activity_tracker_data.shape[0] - 1:
        code_tracker_data, ati_i, is_valid = __handle_current_ati_element(code_tracker_data, activity_tracker_data,
                                                                          code_tracker_data.shape[0] - 1, ati_i, res)
        if is_valid != -1:
            code_tracker_data = __handle_missed_ati_elements(activity_tracker_data, code_tracker_data,
                                                             code_tracker_data.shape[0] - 1, ati_i, ati_i + 1, res, [])
        ati_i += 1

    last_dif = code_tracker_data.shape[0] - __get_dict_lists_size(res)
    if last_dif > 0:
        __add_values_in_ati_dict(res)

    log.info('finish getting activity tracker info')
    return code_tracker_data, res
