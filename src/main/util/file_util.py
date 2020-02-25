# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import re
from typing import Callable

from src.main.util.consts import FILE_SYSTEM_ITEM


def get_content_from_file(file: str):
    with open(file, 'r') as f:
        return f.read().rstrip('\n')


# To get all files or subdirs (depends on the last parameter) from root that match item_condition
# Can be used to get all codetracker files, all data folders, etc.
# Note that all subdirs or files already contain the full path for them
def get_all_file_system_items(root: str, item_condition: Callable, item_type=FILE_SYSTEM_ITEM.FILE.value):
    items = []
    for fs_tuple in os.walk(root):
        for item in fs_tuple[item_type]:
            if item_condition(item):
                items.append(os.path.join(fs_tuple[FILE_SYSTEM_ITEM.PATH.value], item))
    return items


def add_dot_to_not_empty_extension(extension: str):
    if extension and not extension.startswith('.'):
        extension = '.' + extension
    return extension


# if need_to_rуname, it works only for real files because os.rename is called
def change_extension_to(file: str, new_extension: str, need_to_rename=False):
    new_extension = add_dot_to_not_empty_extension(new_extension)
    base, _ = os.path.splitext(file)
    if need_to_rename:
        os.rename(file, base + new_extension)
    return base + new_extension


def pair_in_and_out_files(in_files: list, out_files: list):
    pairs = []
    for in_file in in_files:
        out_file = re.sub(r'in(?=[^in]*$)', 'out', in_file)
        if out_file not in out_files:
            raise ValueError(f'List of out files does not contain a file for {in_file}')
        pairs.append((in_file, out_file))
    return pairs
