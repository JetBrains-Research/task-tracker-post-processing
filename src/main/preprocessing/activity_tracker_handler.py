import logging

import pandas as pd

from src.main.util import consts
from src.main.util.time_util import get_datetime_by_format
from src.main.util.file_util import get_file_name_from_path, get_original_file_name_with_extension, get_parent_folder
from src.main.util.language_util import get_extension_by_language

log = logging.getLogger(consts.LOGGER_NAME)


# Unification of similar activity tracker events. For example, an action Run by pressed the button Run and by
# pressing a combination of buttons is not similar in the source data. After the unification, the function returns a
# new activity tracker data with the union this kind of events
def __unify_activity_tracker_columns(ati_data: pd.DataFrame):
    action_events = consts.ACTIVITY_TRACKER_EVENTS.action_events()
    for index in range(ati_data.shape[0]):
        current_focused_component = ati_data[consts.ACTIVITY_TRACKER_COLUMN.FOCUSED_COMPONENT.value].iloc[index]
        if current_focused_component in action_events:
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


def __get_default_dict_for_at():
    return {
        consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value: [],
        consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value: [],
        consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value: [],
        consts.ACTIVITY_TRACKER_COLUMN.ATI_ID.value: []
    }


def __add_values_in_ati_dict(ati_dict: dict, timestamp="", event_type="", event_data="", ati_id=""):
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].append(timestamp)
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value].append(event_type)
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value].append(event_data)
    ati_dict[consts.ACTIVITY_TRACKER_COLUMN.ATI_ID.value].append(ati_id)


def __add_values_in_ati_dict_by_ati_index(res_dict: dict, activity_tracker_data: pd.DataFrame, index: int, ati_id: str):
    __add_values_in_ati_dict(res_dict,
                            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[index],
                            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value].iloc[index],
                            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value].iloc[index],
                            ati_id)


def __are_same_files(code_tracker_file_name: str, activity_tracker_file_path: str):
    if pd.isnull(activity_tracker_file_path):
        return False
    activity_tracker_file_name = get_file_name_from_path(activity_tracker_file_path)
    return code_tracker_file_name == activity_tracker_file_name


# Insert a row to the dataframe before the row_number position.
# For example, we have the dataset with 1 column and 3 rows: A C D
# If we have row_number = 1 and row_value = B, the function returns the dataset with rows: A B C D
def __insert_row(df: pd.DataFrame, row_number: int, row_value: list):
    if row_number > df.index.max() + 1:
        log.error('Invalid row_number in the method __insert_row')
        raise ValueError('Invalid row_number in the method __insert_row')
    df1 = df[0:row_number]
    df2 = df[row_number:]
    df1.loc[row_number] = row_value
    df_result = pd.concat([df1, df2])
    df_result.index = [*range(df_result.shape[0])]
    return df_result


def preprocess_activity_tracker_data(activity_tracker_data: pd.DataFrame):
    log.info('...starting to unify activity tracker data')
    activity_tracker_data = __unify_activity_tracker_columns(activity_tracker_data)
    log.info('finish to unify activity tracker data')

    log.info('...starting to filter activity tracker data')
    activity_tracker_data = __filter_ati_data(activity_tracker_data)
    log.info('finish to filter activity tracker data')
    return activity_tracker_data


def __create_joined_code_tracker_data_frame(code_tracker_data: pd.DataFrame, res: dict):
    ati_df = pd.DataFrame(res)
    return code_tracker_data.join(ati_df)


def get_full_default_columns_for_at(count_rows: int):
    res = __get_default_dict_for_at()
    for i in range(count_rows):
        __add_values_in_ati_dict(res)
    return res


# Get size of result for activity tracker data
def __get_dict_lists_size(res: dict):
    size = 0
    for key in res.keys():
        if size != 0 and len(res[key]) != size:
            log.error('Lists in the res dict have different sizes')
            raise ValueError('Lists in the res dict have different sizes')
        size = len(res[key])
    return size


def is_last(index, data):
    return index == data.shape[0] - 1


def is_next_ct_valid(ati_time, cur_ct_i, code_tracker_data):
    next_ct_time = get_datetime_by_format(code_tracker_data[consts.CODE_TRACKER_COLUMN.DATE.value].iloc[cur_ct_i + 1])
    return (ati_time - next_ct_time).total_seconds() >= 0


def is_ct_i_filled(ct_i, ati_dict):
    return __get_dict_lists_size(ati_dict) > ct_i


def merge_code_tracker_and_activity_tracker_data(code_tracker_data: pd.DataFrame, activity_tracker_data: pd.DataFrame,
                                                 ati_id: str):
    log.info('Start merging code tracker and activity tracker data')
    res = __get_default_dict_for_at()
    ct_file_name = code_tracker_data[consts.CODE_TRACKER_COLUMN.FILE_NAME.value].iloc[0]
    ct_i = 0

    for ati_i in range(activity_tracker_data.shape[0]):
        activity_tracker_file_path = activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.CURRENT_FILE.value].iloc[
            ati_i]
        if not __are_same_files(ct_file_name, activity_tracker_file_path):
            continue

        ati_time = get_datetime_by_format(
            activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value].iloc[ati_i])

        while not is_last(ct_i, code_tracker_data) and is_next_ct_valid(ati_time, ct_i, code_tracker_data):
            if not is_ct_i_filled(ct_i, res):
                __add_values_in_ati_dict(res)

            ct_i += 1

        if is_ct_i_filled(ct_i, res):
            ct_row = list(code_tracker_data.iloc[ct_i])
            code_tracker_data = __insert_row(code_tracker_data, ct_i + 1, ct_row)
            ct_i += 1

        __add_values_in_ati_dict_by_ati_index(res, activity_tracker_data, ati_i, ati_id)

    log.info('Finish handling the activity tracker file')

    times = code_tracker_data.shape[0] - __get_dict_lists_size(res)
    while times > 0:
        __add_values_in_ati_dict(res)
        times -= 1

    log.info('Finish setting empty values for the last code tracker items')

    code_tracker_data = __create_joined_code_tracker_data_frame(code_tracker_data, res)
    log.info('Finish merging code tracker and activity tracker data')
    return code_tracker_data


def __remove_nan(items: list):
    return list(filter(lambda x: not pd.isnull(x), items))


def get_files_from_ati(activity_tracker_data: pd.DataFrame):
    paths = __remove_nan(activity_tracker_data[consts.ACTIVITY_TRACKER_COLUMN.CURRENT_FILE.value].unique())
    paths_dict = {}
    for current_path in paths:
        path = get_parent_folder(current_path)
        file = get_file_name_from_path(current_path)
        if paths_dict.get(file) is None:
            paths_dict[file] = path
        else:
            if paths_dict[file] != path:
                log.error('Activity tracker data contains several files with the same names')
                raise ValueError('Activity tracker data contains several files with the same names')
    return paths_dict.keys()


def get_ct_name_from_ati_data(ct_file: str, language: consts.LANGUAGE, files_from_at: list):
    log.info('Start getting project file name')
    extension = get_extension_by_language(language)
    hashed_file_name = get_file_name_from_path(ct_file)
    file_name = get_original_file_name_with_extension(hashed_file_name, extension)
    does_contain_name = True
    if files_from_at is not None:
        log.info('Start searching the file_name ' + file_name + ' in activity tracker data')
        if file_name not in files_from_at:
            log.info('Activity tracker data does not contain the original file ' + file_name)
            does_contain_name = False
        log.info('Finish searching the file_name ' + file_name + ' in activity tracker data')

    log.info('Finish getting project file name')
    return file_name, does_contain_name


def handle_ati_file(ati_file: str):
    ati_df = None
    if ati_file:
        ati_df = pd.read_csv(ati_file, encoding=consts.ISO_ENCODING,
                             names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
        ati_df = preprocess_activity_tracker_data(ati_df)
    return ati_df
