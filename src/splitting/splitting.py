import os
from collections import defaultdict

import pandas as pd

# todo: move to consts (create shared const file)
AT_NAME = 'ide-events'
DIFF_MAX = 30
ENCODING = 'ISO-8859-1'


def get_all_files(root):
    cd_files = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if AT_NAME not in name:
                cd_files.append(os.path.join(path, name))
    return cd_files


def get_diffs(data):
    fragment_length = data['fragment'].str.len()
    diffs = [x - y for i, (x, y) in enumerate(zip(fragment_length[:-1], fragment_length[1:]))]
    return diffs


def strong_equal(a, b):
    if pd.isnull(a) and pd.isnull(b):
        return True
    return a == b


def get_task_changes(data):
    task_data = data['chosenTask']
    task_changes = [not strong_equal(t1, t2) for (t1, t2) in zip(task_data[:-1], task_data[1:])]
    return task_changes


def get_task_status_changes(data):
    task_status_data = data['taskStatus']
    task_status_changes = [not strong_equal(s1, s2) for (s1, s2) in zip(task_status_data[:-1], task_status_data[1:])]
    return task_status_changes


def obvious_split(data):
    diffs = get_diffs(data)
    bool_diffs = [d >= DIFF_MAX for d in diffs]

    task_changes = get_task_changes(data)

    task_status_changes = get_task_status_changes(data)

    splits = []

    for i in range(data.shape[0] - 1):
        if bool_diffs[i] and task_changes[i] and task_status_changes[i]:
            splits.append(i)

    return splits


def main():
    path = "../data/data_16_12_19"
    files = get_all_files(path)
    splits = defaultdict(list)
    for file in files:
        data = pd.read_csv(file, encoding=ENCODING)
        s = obvious_split(data)
        splits[len(s)].append([file, s])
    print(len(splits[0]), len(files))


if __name__ == "__main__":
    main()
