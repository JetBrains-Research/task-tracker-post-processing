from src import data_handler as dh
from src import consts
import pandas as pd
import logging
import sys
import os

pd.set_option('display.max_rows', 250)
pd.set_option('display.max_columns', 100)


def __get_data_path():
    args = sys.argv
    if len(args) < 3 or consts.PATH_CMD_ARG not in args:
        raise NameError('List of arguments must have required 1 element: path!')
    try:
        path = args[args.index(consts.PATH_CMD_ARG) + 1]
    except ValueError:
        raise NameError('List of arguments does not have the argument -path')
    except IndexError:
        raise NameError('List of arguments does not have a value after the argument -path')
    return path


def __index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1


def __separate_ati_and_other_files(files, folder):
    ati_file_index = __index_containing_substring(files, consts.ACTIVITY_TRACKER_FILE_NAME)
    ati_file = None
    ati_id = None
    if ati_file_index != -1:
        ati_file = files[ati_file_index]
        del files[ati_file_index]
        ati_id = folder.split('_')[1]
    return files, ati_file, ati_id


def main():
    logging.basicConfig(filename=consts.LOGGER_FILE, level=logging.INFO)
    log = logging.getLogger(consts.LOGGER_NAME)
    try:
        path = __get_data_path()
    except NameError as e:
        log.error(e)
        sys.exit(1)

    if not os.path.isdir(path):
        log.error('There is not a folder! Path is ' + path)
        sys.exit(1)

    # Get child folders for the root folder from generator
    folders = next(os.walk(path))[1]
    for folder in folders:
        files = next(os.walk(path + folder))[2]
        files, ati_file, ati_id = __separate_ati_and_other_files(files, folder)
        for file in files:
            # Todo: add a handler for each file
            # df = pd.read_csv(path + folder + '/' + file, encoding=consts.ENCODING)
            pass
        # Todo: add a handler for activity tracker file


if __name__ == "__main__":
    main()