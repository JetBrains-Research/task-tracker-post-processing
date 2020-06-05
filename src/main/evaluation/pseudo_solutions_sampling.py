import logging
from typing import List, Optional

import numpy as np
import pandas as pd

from src.main.solution_space.consts import TEST_INPUT
from src.main.canonicalization.consts import TREE_TYPE
from src.main.splitting.splitting import find_task_dfs
from src.main.solution_space.path_finder_test_system import TestInput
from src.main.canonicalization.canonicalization import get_trees, are_asts_equal
from src.main.preprocessing.int_experience_adding import convert_to_int_experience
from src.main.preprocessing.intermediate_diffs_removing import __remove_intermediate_diffs_from_df
from src.main.preprocessing.inefficient_statements_removing import __remove_inefficient_statements_from_df
from src.main.solution_space.solution_space_handler import __get_rate, __get_task_index, __get_enum_or_default
from src.main.util.consts import TASK, LANGUAGE, ISO_ENCODING, CODE_TRACKER_COLUMN, TEST_RESULT, DEFAULT_VALUE, \
    INVALID_FILE_FOR_PREPROCESSING, LOGGER_NAME, INT_EXPERIENCE
from src.main.util.file_util import get_all_file_system_items, get_result_folder, get_parent_folder_name, \
    get_name_from_path, write_based_on_language, ct_file_condition, get_extension_from_file

log = logging.getLogger(LOGGER_NAME)


# Finds all fragments that have the chosen task 'pies'. These fragments may not be solutions of chosen task
# because some users chose the wrong task, so let's call them 'pseudo solutions'.
# Run it after running tests, but before splitting
def find_all_pseudo_solutions(path: str, task: TASK, language: LANGUAGE, to_add_int_experience: bool = True,
                              to_remove_incorrect_fragments: bool = True,
                              to_remove_intermediate_diffs: bool = True,
                              to_remove_inefficient_statements: bool = True,
                              result_name_suffix: str = 'pseudo_solutions') -> str:
    files = get_all_file_system_items(path, ct_file_condition)
    result_name_suffix = f'{task.value}_{result_name_suffix}'
    result_folder = get_result_folder(path, result_name_suffix)
    task_index = __get_task_index(task)

    for i, file in enumerate(files):
        log.info(f'Finding pseudo solutions in file {i}/{len(files)}, file: {file}')
        df = pd.read_csv(file, encoding=ISO_ENCODING)
        task_dfs = find_task_dfs(df, task)
        for j, task_df in enumerate(task_dfs):
            log.info(f'Handling df {j}/{len(task_dfs)}')
            if not task_df.empty:
                # Replace test_results for all task with test_result for given task
                task_df[CODE_TRACKER_COLUMN.TESTS_RESULTS.value] = \
                    task_df[CODE_TRACKER_COLUMN.TESTS_RESULTS.value].apply(lambda t_r: __get_rate(t_r, task_index))
                if to_add_int_experience:
                    task_df[CODE_TRACKER_COLUMN.INT_EXPERIENCE.value] = \
                        task_df[CODE_TRACKER_COLUMN.EXPERIENCE.value].apply(convert_to_int_experience)
                if to_remove_incorrect_fragments:
                    task_df = task_df[task_df[CODE_TRACKER_COLUMN.TESTS_RESULTS.value] != TEST_RESULT.INCORRECT_CODE.value]
                if to_remove_intermediate_diffs:
                    task_df = __remove_intermediate_diffs_from_df(task_df)
                if to_remove_inefficient_statements:
                    task_df = __remove_inefficient_statements_from_df(task_df)

                # Change name to get something like pies/ati_207_test_5894859_i.csv
                filename = f'{task.value}/{get_parent_folder_name(file)}_{get_name_from_path(file, False)}_{j}' \
                           f'{get_extension_from_file(file).value}'
                write_based_on_language(result_folder, filename, task_df, language)
    return result_folder


def drop_same_anon_trees(df: pd.DataFrame) -> pd.DataFrame:
    log.info(f'Start dropping same anon trees, df size is {len(df)}')
    df.index = np.arange(0, len(df))
    df_anon_trees = df[CODE_TRACKER_COLUMN.FRAGMENT.value].apply(lambda f: get_trees(f, {TREE_TYPE.ANON})[0]).to_list()
    i = 0
    while i < len(df_anon_trees):
        log.info(f'Handling {i}/{len(df_anon_trees)} anon tree')
        current_anon_tree = df_anon_trees[i]
        j = i + 1
        while j < len(df_anon_trees):
            next_anon_tree = df_anon_trees[j]
            if are_asts_equal(current_anon_tree, next_anon_tree):
                log.info(f'Dropping {j} anon tree')
                df.drop(j, inplace=True)
                df.index = np.arange(0, len(df))
                del df_anon_trees[j]
            else:
                j += 1
        i += 1

    df.index = np.arange(0, len(df))
    log.info(f'Stop dropping same anon trees, df size is {len(df)}')
    return df


# Run it after finding all pseudo solutions to sample n correct test inputs from pseudo solutions. All dataframes with
# pseudo solutions are merged together and filtered according to given arguments (include full solutions or not,
# choose only solutions with given rate, include same anon tree or not). Then, if no specific indices are passed,
# n random fragments are sampled from merged df. If there are less than n fragments in merged df,
# all available fragments are taken. If there are specific indices, these fragments are chosen instead of
# random sampling.
def sample_n_correct_test_inputs(pseudo_solutions_path: str,
                                 n: int,
                                 specific_indices: Optional[List[int]] = None,
                                 to_include_full_solutions: bool = False,
                                 rate: Optional[float] = None,
                                 to_include_same_anon_fragments: bool = False) -> List[TestInput]:
    files = get_all_file_system_items(pseudo_solutions_path, ct_file_condition)
    dfs = list(map(lambda file: pd.read_csv(file, encoding=ISO_ENCODING), files))
    merged_df = pd.concat(dfs, ignore_index=True)

    merged_df = merged_df[merged_df[CODE_TRACKER_COLUMN.AGE.value] != DEFAULT_VALUE.AGE.value]
    merged_df = merged_df[merged_df[CODE_TRACKER_COLUMN.AGE.value] != INVALID_FILE_FOR_PREPROCESSING]
    merged_df = merged_df[merged_df[CODE_TRACKER_COLUMN.EXPERIENCE.value] != DEFAULT_VALUE.INT_EXPERIENCE.value]

    merged_df.reset_index()
    if not to_include_full_solutions:
        merged_df = merged_df[merged_df[CODE_TRACKER_COLUMN.TESTS_RESULTS.value] != TEST_RESULT.FULL_SOLUTION.value]
    if rate is not None:
        merged_df = merged_df[merged_df[CODE_TRACKER_COLUMN.TESTS_RESULTS.value] == rate]

    if not to_include_same_anon_fragments:
        merged_df = drop_same_anon_trees(merged_df)

    if specific_indices:
        n_random_rows = merged_df[merged_df.index.isin(specific_indices)]
    else:
        try:
            n_random_rows = merged_df.sample(n)
        except ValueError:
            log.info(f'There is less than {n} fragments')
            n_random_rows = merged_df

    test_inputs = []
    for i, row in n_random_rows.iterrows():
        log.info(f'random row {i}')
        # Add index in the dataframe to the test_input to ba able identify it later.
        # For example, if we want to sample specific indices again, we can take such indices from previous test_inputs
        test_inputs.append({TEST_INPUT.SOURCE_CODE: row[CODE_TRACKER_COLUMN.FRAGMENT.value].rstrip('\n'),
                            TEST_INPUT.RATE: row[CODE_TRACKER_COLUMN.TESTS_RESULTS.value],
                            TEST_INPUT.AGE: row[CODE_TRACKER_COLUMN.AGE.value],
                            TEST_INPUT.INT_EXPERIENCE:
                                __get_enum_or_default(INT_EXPERIENCE,
                                                      row[CODE_TRACKER_COLUMN.INT_EXPERIENCE.value],
                                                      DEFAULT_VALUE.INT_EXPERIENCE),
                            TEST_INPUT.INDEX: i})
    return test_inputs
