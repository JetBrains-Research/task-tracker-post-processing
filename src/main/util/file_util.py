import os
import shutil


def get_file_name_from_path(file_path: str):
    return file_path.split('/')[-1]


def get_extension_from_file(file_name: str):
    parts = file_name.split(".")
    return parts[-1]


def change_extension_to(file: str, new_extension: str):
    os.rename(file, "".join(file.split(".")[:-1]) + "." + new_extension)


def get_original_file_name(hashed_file_name: str, extension: str):
    return "_".join(hashed_file_name.split('_')[:-4]) + '.' + extension


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


def get_all_files(root: str, condition):
    cd_files = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if condition(name):
                cd_files.append(os.path.join(path, name))
    return cd_files
