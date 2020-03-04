import os

from src.main.plots import consts as plot_consts
from src.main.util.strings_util import crop_string
from src.main.util.file_util import get_parent_folder_name, get_name_from_path


def get_short_name(path: str):
    folder = get_parent_folder_name(path)
    file_name = get_name_from_path(path)
    return os.path.join(folder, crop_string(file_name, plot_consts.SHORT_NAME_LENGTH))
