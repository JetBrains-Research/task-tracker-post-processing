# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Any, Union, Callable

import pandas as pd

from src.main.util import consts
from src.main.util.consts import CODE_TRACKER_COLUMN, ACTIVITY_TRACKER_COLUMN, ISO_ENCODING, EXTENSION
from src.main.util.file_util import get_output_directory, get_all_file_system_items, write_result, \
    extension_file_condition

log = logging.getLogger(consts.LOGGER_NAME)

Column = Union[CODE_TRACKER_COLUMN, ACTIVITY_TRACKER_COLUMN]


def crop_data_by_timestamp(data: pd.DataFrame, column: Column, start_value: Any, end_value: Any = None) -> pd.DataFrame:
    column = column.value
    rows = data.shape[0]
    # If end_value not defined we take data to the end from the dataframe
    if end_value is None:
        end_value = data.iloc[rows - 1][column]
    mask = (data[column] >= start_value) & (data[column] <= end_value)
    return data.loc[mask]


def handle_folder(path: str, output_directory_prefix: str, handle_df: Callable) -> str:
    log.info(f'Start handling the folder {path}')
    output_directory = get_output_directory(path, output_directory_prefix)
    files = get_all_file_system_items(path, extension_file_condition(EXTENSION.CSV))
    for file in files:
        log.info(f'Start handling the file {file}')
        df = pd.read_csv(file, encoding=ISO_ENCODING)
        df = handle_df(df)
        write_result(output_directory, path, file, df)
        log.info(f'Finish handling the file {file}')
    log.info(f'Finish handling the folder {path}')
    return output_directory



