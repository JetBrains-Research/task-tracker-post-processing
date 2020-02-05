import os

import matplotlib.pyplot as plt
import pandas as pd

from src.plots.const import STATUS_COLOR_SIZE_DICT, TASK_COLOR_DICT, STATUS_COLOR_SIZE_DEFAULT, TASK_COLOR_DEFAULT, \
    AT_NAME, ENCODING

def get_extension(file_name):
    return file_name.split('.')[-1]

def get_all_files(root):
    cd_files = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if AT_NAME not in name and get_extension(name) == "csv":
                cd_files.append(os.path.join(path, name))
    return cd_files


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


# show plot with changes of code fragments size, colored according to 'chosenTask' field
def show_colored_fragment_size_plot(path, to_save: bool):
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

    print("showing " + path)
    fig.show()
    if to_save:
        fig.savefig("".join(path.split('.')[:-1]) + ".png")




# show first 5 plots
def main():
    root = "/home/elena/workspaces/python/codetracker-data/data/data_16_12_19"
    files = get_all_files(root)
    for file in files:
        print(file)
        show_colored_fragment_size_plot(file, True)


if __name__ == "__main__":
    main()
