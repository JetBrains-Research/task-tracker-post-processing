# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pandas as pd

from src.main.util.consts import ISO_ENCODING, FILE_SYSTEM_ITEM
from src.main.util.file_util import ct_file_condition, get_all_file_system_items


def print_all_unique_values_in_file(file: str, column: str):
    data = pd.read_csv(file, encoding=ISO_ENCODING)
    ati_events = data[column].dropna().unique().tolist()
    if ati_events:
        print(file)
        print(ati_events)


def print_all_unique_values_in_files(path: str, column: str):
    files = get_all_file_system_items(path, ct_file_condition, FILE_SYSTEM_ITEM.FILE.value)
    for file in files:
        print_all_unique_values_in_file(file, column)
