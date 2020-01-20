from datetime import datetime
from src.main import consts
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


def __get_default_dict_for_ati():
    return {
        consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value: [],
        consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value: [],
        consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value: []
    }


def __add_values_in_ati_dict(ati_dict: dict, timestamp="", event_type="", event_data=""):
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].append(timestamp)
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value].append(event_type)
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value].append(event_data)


def __add_values_in_ati_dict_by_at_index(res_dict: dict, activity_tracker_data: pd.DataFrame, index: int):
    __add_values_in_ati_dict(res_dict,
                             activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[index],
                             activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value].iloc[index],
                             activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value].iloc[index])


def __are_same_files(code_tracker_file_name: str, activity_tracker_file_path: str):
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


def preprocessing_activity_tracker_data(activity_tracker_data: pd.DataFrame):
    log.info('...starting to unify activity tracker data')
    activity_tracker_data = __unification_of_activity_tracker_columns(activity_tracker_data)
    log.info('finish to unify activity tracker data')

    log.info('...starting to filter activity tracker data')
    activity_tracker_data = __filter_ati_data(activity_tracker_data)
    log.info('finish to filter activity tracker data')
    return activity_tracker_data


def __create_join_code_tracker_data_frame(code_tracker_data: pd.DataFrame, res: dict):
    at_df = pd.DataFrame(res)
    return code_tracker_data.join(at_df)


def get_full_default_columns_for_ati(count_rows: int):
    res = __get_default_dict_for_ati()
    for i in range(count_rows):
        __add_values_in_ati_dict(res)
    return res


# Get size of result for activity tracker data
def __get_dict_lists_size(res: dict):
    size = 0
    for key in res.keys():
        if size != 0 and len(res[key]) != size:
            raise ValueError('Lists in the res dict have different sizes')
        size = len(res[key])
    return size


def is_last(index, data):
    return index == data.shape[0] - 1


def is_next_ct_valid(ati_time, cur_ct_i, code_tracker_data):
    next_ct_time = __get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[cur_ct_i + 1])
    return (ati_time - next_ct_time).total_seconds() >= 0


def is_ct_i_filled(ct_i, at_dict):
    return __get_dict_lists_size(at_dict) > ct_i


def merge_code_tracker_and_activity_tracker_data(code_tracker_data: pd.DataFrame, activity_tracker_data: pd.DataFrame):
    res = __get_default_dict_for_ati()
    ct_file_name = code_tracker_data[consts.CODE_TRACKER_COLUMN.FILE_NAME.value].iloc[0]
    ct_i = 0

    for ati_i in range(activity_tracker_data.shape[0]):
        activity_tracker_file_path = activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.CURRENT_FILE.value].iloc[
            ati_i]
        if not __are_same_files(ct_file_name, activity_tracker_file_path):
            continue

        ati_time = __get_datetime_by_format(
            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[ati_i])

        while not is_last(ct_i, code_tracker_data) and is_next_ct_valid(ati_time, ct_i, code_tracker_data):
            if not is_ct_i_filled(ct_i, res):
                __add_values_in_ati_dict(res)

            ct_i += 1

        if is_ct_i_filled(ct_i, res):
            ct_row = list(code_tracker_data.iloc[ct_i])
            code_tracker_data = __insert_row(code_tracker_data, ct_i + 1, ct_row)
            ct_i += 1

        __add_values_in_ati_dict_by_at_index(res, activity_tracker_data, ati_i)

    times = code_tracker_data.shape[0] - __get_dict_lists_size(res)
    while times > 0:
        __add_values_in_ati_dict(res)
        times -= 1

    return __create_join_code_tracker_data_frame(code_tracker_data, res)
