# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import List

import pandas as pd

from src.main.util.consts import FILE_SYSTEM_ITEM, EXTENSION, ISO_ENCODING
from src.main.util.file_util import get_all_file_system_items, language_item_condition, task_item_condition, \
    remove_slash, get_name_from_path, extension_file_condition, does_exist


def check_anonymization(old_files_root: str, new_files_root: str) -> List[str]:
    """
    Find incorrect anonymized files. The file is incorrect if:
     - does not exist in the new folder
     - has more or less rows than in the old folder
    """
    files_with_errors = []
    language_dirs = get_all_file_system_items(new_files_root,
                                              item_condition=language_item_condition,
                                              item_type=FILE_SYSTEM_ITEM.SUBDIR)
    for language_dir in language_dirs:
        task_dirs = get_all_file_system_items(language_dir,
                                              item_condition=task_item_condition,
                                              item_type=FILE_SYSTEM_ITEM.SUBDIR)
        language = get_name_from_path(language_dir, with_extension=False)
        for task_dir in task_dirs:
            task = get_name_from_path(task_dir, with_extension=False)
            old_path = f'{remove_slash(old_files_root)}/{language}/{task}'
            old_files = get_all_file_system_items(old_path,
                                                  item_condition=extension_file_condition(EXTENSION.CSV))
            for old_file in old_files:
                name = get_name_from_path(old_file)
                new_file_path = f'{task_dir}/{name}'
                if not does_exist(new_file_path):
                    files_with_errors.append(new_file_path)
                else:
                    try:
                        new_df = pd.read_csv(new_file_path, encoding=ISO_ENCODING)
                        old_df = pd.read_csv(old_file, encoding=ISO_ENCODING)
                        if new_df.shape[0] != old_df.shape[0]:
                            files_with_errors.append(new_file_path)
                    except pd.errors.EmptyDataError:
                        files_with_errors.append(new_file_path)
    return files_with_errors
