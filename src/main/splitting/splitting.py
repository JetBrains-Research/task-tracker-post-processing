import logging
import sys

import pandas as pd

from src.main.preprocessing.code_tracker_handler import get_ct_language
from main.splitting.tasks_tests_handler import check_tasks, create_in_and_out_dict
from src.main.util import consts
from src.main.util.file_util import ct_file_condition, get_all_file_system_items
from src.main.util.consts import ENCODING, MAX_DIFF_SYMBOLS, CODE_TRACKER_COLUMN, LANGUAGE, PATH_CMD_ARG, TASK
from main.splitting.consts import SPLIT_DICT

FRAGMENT = CODE_TRACKER_COLUMN.FRAGMENT.value

log = logging.getLogger(consts.LOGGER_NAME)


def get_diffs(data: pd.DataFrame):
    fragment_length = data[CODE_TRACKER_COLUMN.FRAGMENT.value].str.len()
    diffs = [x - y for i, (x, y) in enumerate(zip(fragment_length[:-1], fragment_length[1:]))]
    return diffs


def strong_equal(a, b):
    if pd.isnull(a) and pd.isnull(b):
        return True
    return a == b


def get_task_changes(data: pd.DataFrame):
    task_data = data[CODE_TRACKER_COLUMN.CHOSEN_TASK.value]
    task_changes = [not strong_equal(t1, t2) for (t1, t2) in zip(task_data[:-1], task_data[1:])]
    return task_changes


def get_task_status_changes(data: pd.DataFrame):
    task_status_data = data[CODE_TRACKER_COLUMN.TASK_STATUS.value]
    task_status_changes = [not strong_equal(s1, s2) for (s1, s2) in zip(task_status_data[:-1], task_status_data[1:])]
    return task_status_changes


# doesn't work :(
def obvious_split(data: pd.DataFrame):
    diffs = get_diffs(data)
    bool_diffs = [d >= MAX_DIFF_SYMBOLS for d in diffs]
    task_changes = get_task_changes(data)
    task_status_changes = get_task_status_changes(data)
    splits = []

    for i in range(data.shape[0] - 1):
        if bool_diffs[i] and task_changes[i] and task_status_changes[i]:
            splits.append(i)

    return splits


def get_tasks_with_max_rate(tasks: list, test_results: list):
    max_rate = max(test_results)
    indices = [i for i, tr in enumerate(test_results) if tr == max_rate]
    return [tasks[i] for i in indices], max_rate


def find_supposed_splits_by_tests(data: pd.DataFrame, tasks: list, in_and_out_files_dict: dict, supposed_splits: list):
    data[FRAGMENT] = data[FRAGMENT].fillna("")
    language = get_ct_language(data)

    if language is not LANGUAGE.NOT_DEFINED.value:
        data["tasksTests"] = data.apply(lambda row:
                                        check_tasks(tasks, row[FRAGMENT], in_and_out_files_dict, language),
                                        axis=1)
        data.to_csv("/resources/test.csv", sep='\t', encoding=ENCODING)


    # if language is not LANGUAGE.NOT_DEFINED.value:
    #     indices_to_check = range(0, len(fragment_df) - 1)
    #     str_len_indices = str(len(indices_to_check))
    #     log.info("Found " + str_len_indices + " fragments")
    #
    #     for i, f in enumerate(fragment_df):
    #         log.info("Checking fragment " + str(i) + "/" + str_len_indices)
    #         is_code_correct, test_results = check_tasks(tasks, f, in_and_out_files_dict, language)
    #
    #         if not is_code_correct:
    #             continue
    #
    #         correct_fragments_number += 1
    #         max_rate_tasks, max_rate = get_tasks_with_max_rate(tasks, test_results)
    #         if max_rate > 0:
    #             log.info("\nAdded split with rate " + str(max_rate) + ", tasks: " + str(max_rate_tasks) + "\n")
    #             supposed_splits.append({SPLIT_DICT.INDEX.value: i,
    #                                     SPLIT_DICT.RATE.value: max_rate,
    #                                     SPLIT_DICT.TASKS.value: max_rate_tasks})
    #     log.info("Correct fragments: " + str(correct_fragments_number) + "/" + str_len_indices)
    #
    # log.info("\nAll supposed splits: " + str(supposed_splits) + "\n\n\n")
    return supposed_splits


# since lists of tasks have small size, it should work faster than creating a set
def intersect(list_1: list, list_2: list):
    return [e for e in list_1 if e in list_2]


def find_real_splits(supposed_splits: list):
    real_splits = []
    if len(supposed_splits) == 0:
        return real_splits

    prev_split = supposed_splits[0]
    prev_intersected_tasks = prev_split[SPLIT_DICT.TASKS.value]

    for curr_split in supposed_splits:
        curr_intersected_tasks = intersect(prev_intersected_tasks, curr_split[SPLIT_DICT.TASKS.value])
        if len(curr_intersected_tasks) == 0:
            # it means that the supposed task has changed, so we should split on prev_split
            real_splits.append({SPLIT_DICT.INDEX.value: prev_split[SPLIT_DICT.INDEX.value],
                                SPLIT_DICT.RATE.value: prev_split[SPLIT_DICT.RATE.value],
                                SPLIT_DICT.TASKS.value: prev_intersected_tasks})
            prev_intersected_tasks = curr_split[SPLIT_DICT.TASKS.value]
        else:
            prev_intersected_tasks = curr_intersected_tasks

        prev_split = curr_split

    # add the last split
    real_splits.append({SPLIT_DICT.INDEX.value: prev_split[SPLIT_DICT.INDEX.value],
                        SPLIT_DICT.RATE.value: prev_split[SPLIT_DICT.RATE.value],
                        SPLIT_DICT.TASKS.value: prev_intersected_tasks})
    return real_splits


def main():
    logging.basicConfig(filename=consts.LOGGER_FILE, level=logging.INFO)
    args = sys.argv
    path = args[args.index(PATH_CMD_ARG) + 1]

    files = get_all_file_system_items(path, ct_file_condition)
    tasks = [t.value for t in TASK]
    in_and_out_files_dict = create_in_and_out_dict(tasks)

    for i, file in enumerate(files):
        log.info("Start to splitting file" + file + ", " + str(i+1) + "/" + str(len(files)))
        data = pd.read_csv(file, encoding=ENCODING)
        find_supposed_splits_by_tests(data, tasks, in_and_out_files_dict, [])


if __name__ == "__main__":
    main()
