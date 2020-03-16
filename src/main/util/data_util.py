# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import pandas as pd

from typing import Any, Union

from src.main.plots.splitting_plots import create_comparative_filtering_plot
from src.main.util.consts import CODE_TRACKER_COLUMN, ACTIVITY_TRACKER_COLUMN, ISO_ENCODING
from src.main.util.file_util import get_name_from_path, get_parent_folder, create_folder_and_write_df_to_file


def crop_data_by_timestamp(data: pd.DataFrame, column: Union[CODE_TRACKER_COLUMN, ACTIVITY_TRACKER_COLUMN],
                           start_value: Any, end_value: Any = None) -> pd.DataFrame:
    column = column.value
    rows = data.shape[0]
    # If end_value not defined we take data to the end from the dataframe
    if end_value is None:
        end_value = data.iloc[rows - 1][column]
    mask = (data[column] >= start_value) & (data[column] <= end_value)
    return data.loc[mask]


def crop_data_and_save(original_data_path: str, column: Union[CODE_TRACKER_COLUMN, ACTIVITY_TRACKER_COLUMN],
                       start_value: Any, end_value: Any = None, file_name_prefix='crop_',
                       folder_name_prefix='cropped_data', create_sub_folder=True) -> str:
    original_data = pd.read_csv(original_data_path, encoding=ISO_ENCODING)
    cropped_data = crop_data_by_timestamp(original_data, column, start_value, end_value)
    cropped_data_name = file_name_prefix + get_name_from_path(original_data_path)
    cropped_data_folder = get_parent_folder(original_data_path)
    if create_sub_folder:
        cropped_data_folder = os.path.join(cropped_data_folder, folder_name_prefix)
    cropped_data_result_path = os.path.join(cropped_data_folder, cropped_data_name)
    create_folder_and_write_df_to_file(cropped_data_folder, cropped_data_result_path, cropped_data)
    return cropped_data_result_path


def crop_data_and_create_plots(original_data_path: str, column: Union[CODE_TRACKER_COLUMN, ACTIVITY_TRACKER_COLUMN],
                               start_value: Any, end_value: Any = None) -> None:
    cropped_data_result_path = crop_data_and_save(original_data_path, column, start_value, end_value)
    create_comparative_filtering_plot(original_data_path, cropped_data_result_path,
                                      folder_to_save=get_parent_folder(cropped_data_result_path))



