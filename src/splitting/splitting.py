import os
from collections import defaultdict

import pandas as pd

# todo: move to consts (create shared const file)
from src.main.code_tracker_handler import get_language
from src.main.consts import ENCODING, ACTIVITY_TRACKER_FILE_NAME, MAX_DIFF_SYMBOLS, CODE_TRACKER_COLUMN
from src.main.tasks_tests_handler import get_most_likely_tasks


def get_all_files(root: str):
    cd_files = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if ACTIVITY_TRACKER_FILE_NAME not in name:
                cd_files.append(os.path.join(path, name))
    return cd_files


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


def split_with_test(data: pd.DataFrame):
    fragment_df = data[CODE_TRACKER_COLUMN.FRAGMENT.value].astype(str)
    next_fragment = fragment_df.iat[0]
    language = get_language(data)
    splits = []
    prev_split_i = 0

    for ct_i in range(data.shape[0] - 1):
        curr_fragment = next_fragment
        next_fragment = fragment_df.iat[ct_i + 1]
        diff = len(curr_fragment) - len(next_fragment)

        if diff >= MAX_DIFF_SYMBOLS:
            print("max")
            tasks_by_tests, rate = get_most_likely_tasks(curr_fragment, language)
            print(tasks_by_tests, rate, ct_i)


def main():
    path = "/home/elena/workspaces/python/codetracker-data/data/data_16_12_19"
    files = get_all_files(path)
    splits = defaultdict(list)
    for file in files:
        data = pd.read_csv(file, encoding=ENCODING)
        print(file)
        split_with_test(data)
        # s = obvious_split(data)
        # splits[len(s)].append([file, s])
    # print(len(splits[0]), len(files))


if __name__ == "__main__":
    main()
