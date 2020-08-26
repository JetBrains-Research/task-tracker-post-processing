# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pandas as pd

from src.main.util import consts
from src.main.util.data_util import handle_folder
from src.main.util.consts import TASK, TEST_RESULT
from src.main.canonicalization.consts import TREE_TYPE
from src.main.splitting.splitting import unpack_tests_results
from src.main.canonicalization.canonicalization import get_code_from_tree, get_trees
from src.main.util.file_util import get_name_from_path

FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value
TESTS_RESULTS = consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value
FILE_NAME = consts.CODE_TRACKER_COLUMN.FILE_NAME.value


def is_incorrect_fragment(tests_results: str) -> bool:
    return TEST_RESULT.INCORRECT_CODE.value in unpack_tests_results(tests_results, TASK.tasks())


def get_anonymized_code(fragment: str) -> str:
    anon_tree, = get_trees(fragment, {TREE_TYPE.ANON})
    return get_code_from_tree(anon_tree)


def anonymize_code_in_df(df: pd.DataFrame) -> pd.DataFrame:
    # Todo: add other languages???
    # Delete incorrect fragments
    df = df[df.apply(lambda row: not is_incorrect_fragment(row[TESTS_RESULTS]), axis=1)]
    file_name = df[FILE_NAME].unique()[0]
    current_task = TASK(get_name_from_path(file_name, False))
    tasks = TASK.tasks()
    df[TESTS_RESULTS] = df[TESTS_RESULTS].apply(lambda x: unpack_tests_results(x, tasks)[tasks.index(current_task)])
    df[FRAGMENT] = df[FRAGMENT].apply(get_anonymized_code)
    return df


def anonymize_code(path: str, output_directory_prefix: str = 'anonymize_code'):
    return handle_folder(path, output_directory_prefix, anonymize_code_in_df)
