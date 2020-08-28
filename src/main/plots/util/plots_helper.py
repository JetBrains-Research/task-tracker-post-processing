# Copyright (c) by anonymous author(s)

import pandas as pd

from src.main.util.consts import ISO_ENCODING
from src.main.util.file_util import ct_file_condition, get_all_file_system_items


def print_all_unique_values_in_file(file: str, column: str) -> None:
    data = pd.read_csv(file, encoding=ISO_ENCODING)
    ati_events = data[column].dropna().unique().tolist()
    if ati_events:
        print(file)
        print(ati_events)


def print_all_unique_values_in_files(path: str, column: str) -> None:
    files = get_all_file_system_items(path, ct_file_condition)
    for file in files:
        print_all_unique_values_in_file(file, column)
