import pandas as pd
from src.main.util import consts
from src.main.util.consts import TASK
from src.main.util.consts import CODE_TRACKER_COLUMN
from src.main.util.data_util import crop_data_and_create_plots
FOLDER = 'folder'
FILE = 'file'
START = 'start'
END = 'end'
sources = [
    {
        FOLDER: TASK.ZERO.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/is_zero/ati_205_test_3924_8338274_1564691555063.0962_ca74f2862614299a8409989a9c593be220f1fb79_0.csv',
        START: 3928
    },
    {
        FOLDER: TASK.ZERO.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/is_zero/ati_206_test_3927_6753787_1365530703655.7397_2af58a25bc4cff24a64280a6833050b6b469b623_0.csv',
        START: 4100
    },
    {
        FOLDER: TASK.ZERO.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/is_zero/ati_241_test_8155_1377339_40104989606.44157_1641f0fb729baa91ebef5c5f99f451ff13027465_0.csv',
        START: 14385
    },
    {
        FOLDER: TASK.ZERO.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/is_zero/di_231_1_4900_25169199_1517086558343.152_0c101a17cc97689abd694b24fef5e865373bbdb2_0.csv',
        START: 1992
    },
    {
        FOLDER: TASK.MAX_3.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/max_3/ati_208_скибидибамбони_8207_31794900_605885085965.2665_90e2b7eb3771965fca35f7af63a79c30187e2fc9_0.csv',
        START: 2131
    },
    {
        FOLDER: TASK.MAX_3.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/max_3/ati_226_nnn_7993_28784416_194213531538.28998_f693d0602d134e455a597233273a7f8e8fbc813f_0.csv',
        START: 1279
    },
    {
        FOLDER: TASK.MAX_3.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/max_3/ati_338_main_6847_4337348_344732819754.7162_c1748bae205d445b50e5ae66f8f8e5cdb9a06809_0.csv',
        START: 2800
    },
    {
        FOLDER: TASK.MAX_DIGIT.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/max_digit/ati_219_smth_3875_692915_1076739655245.9308_1afbf84de1ff6fbffc72125b28e96fe64117f0fd_0.csv',
        START: 14569
    },
    {
        FOLDER: TASK.MAX_DIGIT.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/max_digit/ati_236_game_7889_21041224_817720292175.449_608b5427041bf45d8c6f0e17e294792cb238b462_0.csv',
        START: 9337,
        END: 12019
    },
    {
        FOLDER: TASK.MAX_DIGIT.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/max_digit/di_209_newPt_4611_12390667_762127414508.162_9661c72753a7a42f09a59ca4312b1f38e63fd711_0.csv',
        START: 5572
    },
    {
        FOLDER: TASK.PIES.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/pies/ati_226_nnn_7993_28784416_194213531538.28998_f693d0602d134e455a597233273a7f8e8fbc813f_0.csv',
        START: 6125
    },
    {
        FOLDER: TASK.PIES.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/pies/ati_236_game_7889_21041224_817720292175.449_608b5427041bf45d8c6f0e17e294792cb238b462_0.csv',
        START: 2989
    },
    {
        FOLDER: TASK.PIES.value,
        FILE: '/home/elena/workspaces/python/codetracker-data/data/python_2_cropped/pies/di_231_1_4900_25169199_1517086558343.152_0c101a17cc97689abd694b24fef5e865373bbdb2_0.csv',
        START: 5319
    },
]

for source in sources:
    print(source[FILE])
    crop_data_and_create_plots(source[FILE], CODE_TRACKER_COLUMN.TIMESTAMP, source[START],
                               end_value=source.get(END, None),
                               file_name_prefix='')


