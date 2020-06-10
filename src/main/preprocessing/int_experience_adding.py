
import pandas as pd

from src.main.util.file_util import get_all_file_system_items, get_output_directory, write_result
from src.main.util.consts import ISO_ENCODING, CODE_TRACKER_COLUMN, INT_EXPERIENCE, DEFAULT_VALUE


def convert_to_int_experience(experience: str) -> int:
    try:
        int_experience = INT_EXPERIENCE[experience].value
        return int_experience
    except KeyError:
        return DEFAULT_VALUE.INT_EXPERIENCE.value


def add_int_experience(path: str, output_directory_prefix: str = 'int_exp') -> str:
    output_directory = get_output_directory(path, output_directory_prefix)
    files = get_all_file_system_items(path)
    for file in files:
        df = pd.read_csv(file, encoding=ISO_ENCODING)
        df[CODE_TRACKER_COLUMN.INT_EXPERIENCE.value] = \
            df[CODE_TRACKER_COLUMN.EXPERIENCE.value].apply(convert_to_int_experience)
        write_result(output_directory, path, file, df)
    return output_directory
