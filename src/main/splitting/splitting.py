import ast
import logging

import pandas as pd

from src.main.util import consts
from main.util.consts import ISO_ENCODING

log = logging.getLogger(consts.LOGGER_NAME)

TESTS_RESULTS = consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value
CHOSEN_TASK = consts.CODE_TRACKER_COLUMN.CHOSEN_TASK.value
TASK_STATUS = consts.CODE_TRACKER_COLUMN.TASK_STATUS.value


def get_solved_task(tests_results: str):
    tests_results = list(map(int, ast.literal_eval(tests_results)))
    tasks = consts.TASK.tasks()
    solved_tasks = [t for i, t in enumerate(tasks) if tests_results[i] == 1]
    if len(solved_tasks) == 0:
        log.info(f'No solved tasks found, tests results: {tests_results}')
        return ''
    elif len(solved_tasks) == 1:
        log.info(f'Found solved task {solved_tasks[0]}, tests results: {tests_results}')
        return solved_tasks[0]
    else:
        log.error(f'Several tasks are solved: {solved_tasks}, tests results: {tests_results}')
        raise ValueError(f'Several tasks are solved: {solved_tasks}, tests results: {tests_results}')


def find_next_solved_task(cur_i: int, df: pd.DataFrame):
    df = df.iloc[cur_i:]
    next_task_df = df[CHOSEN_TASK].where(df[CHOSEN_TASK] != '').dropna()
    if not next_task_df.empty:
        return next_task_df.iloc[0]
    return ''


def find_splits(ct_file: str):
    log.info(f'Start splitting file {ct_file}')
    ct_df = pd.read_csv(ct_file, encoding=ISO_ENCODING)
    # fill chosen task according to solved task
    ct_df[CHOSEN_TASK] = ct_df.apply(lambda row: get_solved_task(row[TESTS_RESULTS]), axis=1)

    # change task status according to chosen task
    ct_df.loc[ct_df.chosenTask == '', TASK_STATUS] = 'nan'
    ct_df.loc[ct_df.chosenTask != '', TASK_STATUS] = consts.TASK_STATUS.SOLVED.value

    # fill chosen task
    ct_df[CHOSEN_TASK] = ct_df.apply(lambda row: find_next_solved_task(row.name, ct_df), axis=1)
    return ct_df
