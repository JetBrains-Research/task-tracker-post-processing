import os
import shutil
from typing import Callable

import pandas as pd

from src.main.util.consts import ACTIVITY_TRACKER_FILE_NAME, FILE_SYSTEM_ITEM, ATI_DATA_FOLDER, \
    DI_DATA_FOLDER, ISO_ENCODING, LANGUAGE, UTF_ENCODING

'''
To understand correctly these functions' behavior you can see examples in a corresponding test folder.
Also, the naming convention can be helpful:
    folder_name -- just name without any slashes; 
for example, folder_name for the last folder in 'path/data/folder/' is 'folder'
    file_name -- similarly to the folder_name, but may contain its extension;
for example, file_name for the file 'path/data/file.csv' can be 'file.csv' or just 'file' (see get_file_name_from_path)
    file, folder, directory -- contain the full path
    extension -- we consider, that if extension is not empty, it is with a dot, because of os.path implementation; 
If extension is passed without any dots, it will be added (for example, see change_extension_to)
'''


def remove_slash(path: str):
    if path and path[-1] == '/':
        path = path[:-1]
    return path


def add_slash(path: str):
    if not path or path[-1] != '/':
        path += '/'
    return path


def get_file_name_from_path(path: str, with_extension=True):
    head, tail = os.path.split(path)
    # tail can be empty if '/' is at the end of the path
    file_name = tail or os.path.basename(head)
    if not with_extension:
        file_name = os.path.splitext(file_name)[0]
    elif not get_extension_from_file(file_name):
        raise ValueError('Cannot get file name with extension, because the passed path does not contain it')
    return file_name


# not empty extensions are returned with a dot, for example, '.txt'
# if file has no extensions, an empty one ('') is returned
def get_extension_from_file(file: str):
    return os.path.splitext(file)[1]


def add_dot_to_not_empty_extension(extension: str):
    if extension and extension[0] != '.':
        extension = '.' + extension
    return extension


# works only for real files, because os.rename is called, raises FileNotFoundError in case of not real file
def change_extension_to(file: str, new_extension: str):
    add_dot_to_not_empty_extension(new_extension)
    base, _ = os.path.splitext(file)
    os.rename(file, base + new_extension)


def get_parent_folder(path: str, to_add_slash=False):
    path = remove_slash(path)
    parent_folder = '/'.join(path.split('/')[:-1])
    if to_add_slash:
        parent_folder = add_slash(parent_folder)
    return parent_folder


def get_parent_folder_name(path: str):
    path = remove_slash(path)
    return path.split('/')[-2]


def get_original_file_name(hashed_file_name: str):
    return '_'.join(hashed_file_name.split('_')[:-4])


def get_original_file_name_with_extension(hashed_file_name: str, extension: str):
    add_dot_to_not_empty_extension(extension)
    return get_original_file_name(hashed_file_name) + extension


def get_content_from_file(file: str):
    with open(file, 'r') as f:
        return f.read().rstrip('\n')


def create_file(content: str, extension: str, file_without_extension: str):
    add_dot_to_not_empty_extension(extension)
    with open(file_without_extension + extension, 'w') as f:
        f.write(content)


def remove_file(file: str):
    if os.path.isfile(file):
        os.remove(file)


def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
        
def remove_directory(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=True)


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


def csv_file_condition(name: str):
    return get_extension_from_file(name) == 'csv'


# to get all codetracker files
def ct_file_condition(name: str):
    return ACTIVITY_TRACKER_FILE_NAME not in name and csv_file_condition(name)


# to get all subdirs that contain ct and ati data
def data_subdirs_condition(name: str):
    return ATI_DATA_FOLDER in name or DI_DATA_FOLDER in name


# to get path to the result folder that is near to the original folder
# and has the same name but with a suffix added at the end
def get_result_folder(folder: str, result_name_suffix: str):
    result_folder_name = get_file_name_from_path(folder) + '_' + result_name_suffix
    return os.path.join(get_parent_folder(folder), result_folder_name)


def create_folder_and_write_df_to_file(folder_to_write: str, file_to_write: str, df: pd.DataFrame):
    create_directory(folder_to_write)

    # get error with this encoding=ENCODING on ati_225/153e12:
    # "UnicodeEncodeError: 'latin-1' codec can't encode character '\u0435' in position 36: ordinal not in range(256)"
    # So change it then to 'utf-8'
    try:
        df.to_csv(file_to_write, encoding=ISO_ENCODING, index=False)
    except UnicodeEncodeError:
        df.to_csv(file_to_write, encoding=UTF_ENCODING, index=False)


# to write a dataframe to the result_folder remaining the same file structure as it was before
# for example, for path home/codetracker/data and file home/codetracker/data/folder1/folder2/ati_566/file.csv
# the dataframe will be written to result_folder/folder1/folder2/ati_566/file.csv
def write_result(result_folder: str, path: str, file: str, df: pd.DataFrame):
    # check if file is in a path, otherwise we cannot reproduce its structure inside of result_folder
    if path != file[:len(path)]:
        raise ValueError('File is not in a path')
    path_from_result_folder_to_file = file[len(path):]
    file_to_write = os.path.join(result_folder, path_from_result_folder_to_file)
    folder_to_write = get_parent_folder(file_to_write)
    create_folder_and_write_df_to_file(folder_to_write, file_to_write, df)


# to write a dataframe to the result_folder based on the language and remaining only the parent folder structure
# for example, for file path/folder1/folder2/ati_566/file.csv and python language the dataframe will be
# written to result_folder/python/ati_566/file.csv
def write_based_on_language(result_folder: str, file: str, df: pd.DataFrame, language=LANGUAGE.PYTHON.value):
    folder_to_write = os.path.join(result_folder, language, get_parent_folder_name(file))
    file_to_write = os.path.join(folder_to_write, get_file_name_from_path(file))
    create_folder_and_write_df_to_file(folder_to_write, file_to_write, df)
