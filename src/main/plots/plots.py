import logging
import sys

import matplotlib.pyplot as plt
import pandas as pd

from main.splitting.tasks_tests_handler import create_in_and_out_dict
from src.main.util.consts import ENCODING, LOGGER_NAME, LOGGER_FILE, TASK
from src.main.util.file_util import get_all_file_system_items, ct_file_condition
from main.plots.consts import STATUS_COLOR_SIZE_DICT, TASK_COLOR_DICT, STATUS_COLOR_SIZE_DEFAULT, TASK_COLOR_DEFAULT, \
    DATA_ROOT_ARG
from main.splitting.consts import SPLIT_DICT
from main.splitting import find_real_splits, find_supposed_splits_by_tests

log = logging.getLogger(LOGGER_NAME)


def show_fragment_size_plot(data):
    fragment_size = data.loc[:, 'fragment'].str.len()
    plt.plot(fragment_size, 'b-')
    plt.ylabel("fragment size")
    plt.show()


def find_color_size(value):
    return STATUS_COLOR_SIZE_DICT.get(value, STATUS_COLOR_SIZE_DEFAULT)


def get_short_name(path):
    folder = path.split('/')[-2]
    file_name = path.split('/')[-1]
    folder_with_name = folder + '/' + file_name[:10] + '...' + file_name[-10:]
    return folder_with_name


def add_splits_on_plot(splits):
    for s in splits:
        plt.axvline(x=s, color='k', linestyle='-')


# show plot with changes of code fragments size, colored according to 'chosenTask' field
def show_colored_fragment_size_plot(path, to_save=False, splits=[]):
    data = pd.read_csv(path, encoding=ENCODING)

    fig, ax = plt.subplots()

    fragment_color_size = data['taskStatus'].apply(find_color_size)
    fragment_size = data.loc[:, 'fragment'].str.len()

    task_color = data['chosenTask'].apply(lambda t: TASK_COLOR_DICT.get(t, TASK_COLOR_DEFAULT))
    task_y = -1

    for i in range(len(fragment_size)):
        ax.plot(i, fragment_size[i], fragment_color_size[i][0], ms=fragment_color_size[i][1])
        ax.plot(i, task_y, task_color[i])

    plt.xlabel("change number")
    plt.ylabel("fragment size")
    plt.title(get_short_name(path))

    add_splits_on_plot(splits)
    if to_save:
        log.info("Saving" + path)
        path_parts = path.split('/')
        fig.savefig("/".join(path_parts[:-1]) + "/split_" + path_parts[-1].split('.')[0] + ".png")

    log.info("Showing " + path)
    fig.show()


def main():
    logging.basicConfig(filename=LOGGER_FILE, level=logging.INFO)

    args = sys.argv
    root = args[args.index(DATA_ROOT_ARG) + 1]
    files = get_all_file_system_items(root, ct_file_condition)

    tasks = [t.value for t in TASK]
    in_and_out_files_dict = create_in_and_out_dict(tasks)

    for i, file in enumerate(files):
        log.info("Start to splitting file" + file + ", " + str(i+1) + "/" + str(len(files)))
        data = pd.read_csv(file)
        # prev_splits = handle_logs()
        prev_splits = []
        splits = find_real_splits(find_supposed_splits_by_tests(data, tasks, in_and_out_files_dict, prev_splits))
        splits_indices = list(map(lambda s: s[SPLIT_DICT.INDEX.value], splits))
        show_colored_fragment_size_plot(file, True, splits_indices)


if __name__ == "__main__":
    main()
