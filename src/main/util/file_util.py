import os
import shutil

from src.main.util.consts import ACTIVITY_TRACKER_FILE_NAME, FILE_SYSTEM_ITEM, DATA_FOLDER_WITH_AT, \
    DATA_FOLDER_WITHOUT_AT


def remove_slash(path):
    if path[-1] == '/':
        path = path[:-1]
    return path


def add_slash(path):
    if path[-1] != '/':
        path += '/'
    return path


def get_file_name_from_path(file_path: str, with_extension=True):
    file_path = remove_slash(file_path)
    file_name = file_path.split('/')[-1]
    if not with_extension:
        file_name = file_name.split('.')[0]
    return file_name


def get_extension_from_file(file: str):
    return file.split(".")[-1]


def get_parent_folder(file_path: str, to_add_slash=False):
    file_path = remove_slash(file_path)
    parent_folder = "/".join(file_path.split('/')[:-1])
    if to_add_slash:
        parent_folder = add_slash(parent_folder)
    return parent_folder


def get_parent_folder_name(file_path: str):
    file_path = remove_slash(file_path)
    return file_path.split('/')[-2]


def change_extension_to(file: str, new_extension: str):
    os.rename(file, "".join(file.split(".")[:-1]) + "." + new_extension)


def get_original_file_name(hashed_file_name: str):
    return "_".join(hashed_file_name.split('_')[:-4])


def get_original_file_name_with_extension(hashed_file_name: str, extension: str):
    return get_original_file_name(hashed_file_name) + '.' + extension


def remove_file(file: str):
    if os.path.isfile(file):
        os.remove(file)


def get_content_from_file(file: str):
    with open(file, 'r') as f:
        return f.read().rstrip("\n")


def create_file(content: str, extension: str, file_name: str):
    with open(file_name + '.' + extension, 'w') as f:
        f.write(content)


def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
        
def remove_directory(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=True)


# To get all files or subdirs (depends on the last parameter) from root that match item_condition
# Can be used to get all codetracker files, all data folders, etc.
# Note that all subdirs or files already contain the full path for them
def get_all_file_system_items(root: str, item_condition, item_type=FILE_SYSTEM_ITEM.FILE.value):
    items = []
    for fs_tuple in os.walk(root):
        for item in fs_tuple[item_type]:
            if item_condition(item):
                items.append(os.path.join(fs_tuple[FILE_SYSTEM_ITEM.PATH.value], item))
    return items


def csv_file_condition(name):
    return get_extension_from_file(name) == "csv"


# to get all codetracker files
def ct_file_condition(name):
    return ACTIVITY_TRACKER_FILE_NAME not in name and csv_file_condition(name)


# to get all subdirs that contain ct and at data
def data_subdirs_condition(name):
    return DATA_FOLDER_WITH_AT in name or DATA_FOLDER_WITHOUT_AT in name


# to get path to the result folder that is near to the original folder
# and has the same name but with a suffix added at the end
def get_result_folder(folder, result_name_suffix):
    result_folder_name = get_file_name_from_path(folder) + "_" + result_name_suffix
    return os.path.join(get_parent_folder(folder), result_folder_name)

