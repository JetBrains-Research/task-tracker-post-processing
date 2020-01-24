from src.main import consts, activity_tracker_handler as ath, code_tracker_handler as dh
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


def __get_real_ati_file_index(path: str, files: list, ati_key: str):
    sniffer = csv.Sniffer()
    sample_bytes = 1024
    count_ati = 0
    ati_index = -1
    for i, f in enumerate(files):
        if ati_key in f:
            if not sniffer.has_header(open(path + '/' + f, encoding=consts.ENCODING).read(sample_bytes)):
                count_ati += 1
                ati_index = i
                if count_ati >= 2:
                    raise ValueError('Count of activity tracker files is more 1')
    return ati_index


def __separate_ati_and_other_files(files: list, folder: str, full_path: str):
    ati_file_index = __get_real_ati_file_index(full_path, files, consts.ACTIVITY_TRACKER_FILE_NAME)
    ati_file = None
    ati_id = None
    if ati_file_index != -1:
        ati_file = files[ati_file_index]
        del files[ati_file_index]
        ati_id = folder.split('_')[1]
    return files, ati_file, ati_id


def __get_folders_for_handling(path: str):
    # Get child folders for the root folder from generator and remove result folder
    return list(filter(lambda x: consts.RESULT_FOLDER not in x, next(os.walk(path))[1]))


def __write_result(path: str, file: str, result_df: pd.DataFrame):
    path += '/' + consts.RESULT_FOLDER + '/' + file
    result_df.to_csv(path, encoding=consts.ENCODING, index=False)


def main():
    logging.basicConfig(filename=consts.LOGGER_FILE, level=logging.INFO)
    log = logging.getLogger(consts.LOGGER_NAME)
    try:
        path = __get_data_path()
    except NameError as e:
        log.error(e)
        print(e)
        sys.exit(1)

    if not os.path.isdir(path):
        error_message = 'There is not a folder! Path is ' + path
        log.error(error_message)
        print(error_message)
        sys.exit(1)

    # Add / to the end of the path
    if path[-1] != '/':
        path += '/'

    folders = __get_folders_for_handling(path)
    for folder in folders:
        log.info('Start handling the folder ' + folder)
        files = next(os.walk(path + folder))[2]
        # Todo: maybe add 'try except'
        files, ati_file, ati_id = __separate_ati_and_other_files(files, folder, path + folder)
        ati_df = None
        files_from_ati = None
        if ati_file:
            ati_df = pd.read_csv(path + folder + '/' + ati_file, encoding=consts.ENCODING,
                                 names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
            files_from_ati = ath.get_file_names_from_ati(ati_df)
            ati_df = ath.preprocessing_activity_tracker_data(ati_df)

        for file in files:
            log.info('Start handling the file ' + file)
            ct_df = pd.read_csv(path + folder + '/' + file, encoding=consts.ENCODING)
            language = dh.get_language(ct_df)
            ct_df[consts.CODE_TRACKER_COLUMN.LANGUAGE.value] = language
            ct_df[consts.CODE_TRACKER_COLUMN.FILE_NAME.value], ati_is_valid = ath.get_file_name_from_ati_data(file,
                                                                                                             language,
                                                                                                             files_from_ati)

            ct_df[consts.CODE_TRACKER_COLUMN.AGE.value] = dh.profile_column_handler(ct_df,
                                                                                    consts.CODE_TRACKER_COLUMN.AGE.value,
                                                                                    consts.DEFAULT_VALUES.AGE.value)
            ct_df[consts.CODE_TRACKER_COLUMN.EXPERIENCE.value] = dh.profile_column_handler(ct_df,
                                                                                           consts.CODE_TRACKER_COLUMN.EXPERIENCE.value,
                                                                                           consts.DEFAULT_VALUES.EXPERIENCE.value)

            if ati_file is None or not ati_is_valid:
                ati_new_data = pd.DataFrame(ath.get_full_default_columns_for_ati(ct_df.shape[0]))
                ct_df = ct_df.join(ati_new_data)
            else:
                ct_df = ath.merge_code_tracker_and_activity_tracker_data(ct_df, ati_df, ati_id)
            __write_result(path, file, ct_df)

            pass
        log.info('Finish handling the folder ' + folder)


if __name__ == "__main__":
    main()
