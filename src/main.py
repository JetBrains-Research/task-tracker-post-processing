from src import data_handler as dh
from src import activity_tracker_handler as ath
from src import consts
import pandas as pd
import logging
import csv
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


def __count_containing_substring(list_of_string: list, substring: str):
    count = 0
    for i, s in enumerate(list_of_string):
        if substring in s:
            count += 1
    return count


def __index_containing_substring(list_of_string: list, substring: str):
    for i, s in enumerate(list_of_string):
        if substring in s:
            return i
    return -1


def __get_real_ati_file_index(path: str, files: list, ati_key: str):
    sniffer = csv.Sniffer()
    sample_bytes = 1024
    for i, f in enumerate(files):
        if ati_key in f:
            if not sniffer.has_header(open(path + '/' + f, encoding=consts.ENCODING).read(sample_bytes)):
                return i
    return -1


def __separate_ati_and_other_files(files: list, folder: str, full_path: str):
    count_ati = __count_containing_substring(files, consts.ACTIVITY_TRACKER_FILE_NAME)
    ati_file = None
    ati_id = None
    if count_ati > 1:
        ati_file_index = __get_real_ati_file_index(full_path, files, consts.ACTIVITY_TRACKER_FILE_NAME)
    else:
        ati_file_index = __index_containing_substring(files, consts.ACTIVITY_TRACKER_FILE_NAME)
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

    # Add / to the end of the path
    if path[-1] != '/':
        path += '/'

    # Get child folders for the root folder from generator
    folders = next(os.walk(path))[1]
    for folder in folders:
        log.info('Start to handle the folder ' + folder)
        files = next(os.walk(path + folder))[2]
        files, ati_file, ati_id = __separate_ati_and_other_files(files, folder, path + folder)
        ati_df = None
        if ati_file:
            ati_df = pd.read_csv(path + folder + '/' + ati_file, encoding=consts.ENCODING,
                                 names=consts.ACTIVITY_TRACKER_COLUMNS)
        for file in files:
            log.info('Start to handle the file ' + file)
            ct_df = pd.read_csv(path + folder + '/' + file, encoding=consts.ENCODING)
            if ati_file is None:
                ati_new_data = pd.DataFrame(ath.get_full_default_columns_for_ati(ct_df.shape[0]))
            else:
                ati_new_data = pd.DataFrame(ath.merge_code_tracker_and_activity_tracker_data(ct_df, ati_df))
            ct_df = ct_df.join(ati_new_data)
            # Todo: add a handler for each file - profile, language, id activity tracker
            pass
        log.info('Finish to handle the folder ' + folder)


if __name__ == "__main__":
    main()
