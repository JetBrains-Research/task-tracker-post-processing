# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from typing import Tuple

import pandas as pd

from src.main.util import consts
from src.test.test_util import LoggedTest
from src.main.preprocessing import activity_tracker_handler as ath

ath_test_folder = os.path.join(consts.TEST_DATA_PATH, 'preprocessing/activity_tracker_handler')

right_df = pd.DataFrame({'Number': [10, 11, 12, 13, 14], 'Key': ['A', 'B', 'C', 'D', 'E']})


def get_data_for_insert_by_index_test() -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_df = pd.DataFrame({'Number': [10, 12, 13, 14],
                            'Key': ['A', 'C', 'D', 'E']})
    new_row_number = 1
    new_row_value = [11, 'B']
    res_test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    return res_test_df, right_df


def get_data_for_insert_two_times() -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_df = pd.DataFrame({'Number': [10, 12, 14],
                            'Key': ['A', 'C', 'E']})
    new_row_number = 1
    new_row_value = [11, 'B']
    test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    new_row_number = 3
    new_row_value = [13, 'D']
    res_test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    return res_test_df, right_df


def get_data_for_insert_at_the_beginning_test() -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_df = pd.DataFrame({'Number': [11, 12, 13, 14],
                            'Key': ['B', 'C', 'D', 'E']})
    new_row_number = 0
    new_row_value = [10, 'A']
    res_test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    return res_test_df, right_df


def get_data_for_insert_at_the_end_test() -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_df = pd.DataFrame({'Number': [10, 11, 12, 13],
                            'Key': ['A', 'B', 'C', 'D']})
    new_row_number = 4
    new_row_value = [14, 'E']
    res_test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    return res_test_df, right_df


def get_data_for_unification_test() -> Tuple[pd.DataFrame, pd.DataFrame]:
    folder = 'preparing'
    ati_df = pd.read_csv(os.path.join(ath_test_folder, folder, 'ide-events_1.csv'), encoding=consts.ISO_ENCODING,
                         names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    ati_df = ath.__unify_activity_tracker_columns(ati_df)

    ati_df_right = pd.read_csv(os.path.join(ath_test_folder, folder, 'ide-events_1_uni_res.csv'),
                               encoding=consts.ISO_ENCODING,
                               names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    return ati_df, ati_df_right


def get_data_for_filter_test() -> Tuple[pd.DataFrame, pd.DataFrame]:
    folder = 'preparing'
    ati_df = pd.read_csv(os.path.join(ath_test_folder, folder, 'ide-events_1_uni_res.csv'),
                         encoding=consts.ISO_ENCODING,
                         names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    ati_df = ath.__filter_ati_data(ati_df)

    ati_df_right = pd.read_csv(os.path.join(ath_test_folder, folder, 'ide-events_1_filter_res.csv'),
                               encoding=consts.ISO_ENCODING,
                               names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    return ati_df, ati_df_right


def __replace_nan_in_ati_columns(merged_data: pd.DataFrame) -> pd.DataFrame:
    activity_tracker_columns = [consts.ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value,
                                consts.ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value,
                                consts.ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value,
                                consts.ACTIVITY_TRACKER_COLUMN.ATI_ID.value]
    for column in activity_tracker_columns:
        merged_data[column].fillna('', inplace=True)
    return merged_data


def get_data_for_merging_test_1() -> Tuple[pd.DataFrame, pd.DataFrame]:
    ati_folder = 'ati_1'
    ati_df = pd.read_csv(os.path.join(ath_test_folder, ati_folder, 'ide-events_1.csv'), encoding=consts.ISO_ENCODING,
                         names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    ati_df = ath.preprocess_activity_tracker_data(ati_df)
    ct_df = pd.read_csv(os.path.join(ath_test_folder, ati_folder, 'task_1.csv'), encoding=consts.ISO_ENCODING)
    ct_df_right = __replace_nan_in_ati_columns(
        pd.read_csv(os.path.join(ath_test_folder, ati_folder, 'union_task_1.csv'), encoding=consts.ISO_ENCODING))

    ct_df = ath.merge_code_tracker_and_activity_tracker_data(ct_df, ati_df, 'id')
    # ct_df.to_csv(file_name, sep='\t')

    return ct_df, ct_df_right


def get_data_for_merging_test_2() -> Tuple[pd.DataFrame, pd.DataFrame]:
    ati_folder = 'ati_1'
    ati_df = pd.read_csv(os.path.join(ath_test_folder, ati_folder, 'ide-events_1.csv'), encoding=consts.ISO_ENCODING,
                         names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    ati_df = ath.preprocess_activity_tracker_data(ati_df)

    ct_df = pd.read_csv(os.path.join(ath_test_folder, ati_folder, 'task_2.csv'), encoding=consts.ISO_ENCODING)
    ct_df_right = __replace_nan_in_ati_columns(
        pd.read_csv(os.path.join(ath_test_folder, ati_folder, 'union_task_2.csv'), encoding=consts.ISO_ENCODING))

    ct_df = ath.merge_code_tracker_and_activity_tracker_data(ct_df, ati_df, 'id')

    return ct_df, ct_df_right


def get_data_for_merging_test_3() -> Tuple[pd.DataFrame, pd.DataFrame]:
    ati_folder = 'ati_1'
    ati_df = pd.read_csv(os.path.join(ath_test_folder, ati_folder, 'ide-events_1.csv'), encoding=consts.ISO_ENCODING,
                         names=consts.ACTIVITY_TRACKER_COLUMN.activity_tracker_columns())
    ati_df = ath.preprocess_activity_tracker_data(ati_df)

    ct_df = pd.read_csv(os.path.join(ath_test_folder, ati_folder, 'task_1_test_2.csv'), encoding=consts.ISO_ENCODING)
    ct_df_right = __replace_nan_in_ati_columns(
        pd.read_csv(os.path.join(ath_test_folder, ati_folder, 'union_task_1_test_2.csv'), encoding=consts.ISO_ENCODING))

    ct_df = ath.merge_code_tracker_and_activity_tracker_data(ct_df, ati_df, 'id')

    return ct_df, ct_df_right


def is_equals(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    return df_1.equals(df_2)


class TestDataFrameMethods(LoggedTest):

    def test_insert_by_index(self) -> None:
        res_test_df, res_right_df = get_data_for_insert_by_index_test()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_data_for_insert_two_times(self) -> None:
        res_test_df, res_right_df = get_data_for_insert_two_times()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_data_for_insert_at_the_beginning_test(self) -> None:
        res_test_df, res_right_df = get_data_for_insert_at_the_beginning_test()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_data_for_insert_at_the_end_test(self) -> None:
        res_test_df, res_right_df = get_data_for_insert_at_the_end_test()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_unification_data(self) -> None:
        res_test_df, res_right_df = get_data_for_unification_test()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_filter_data(self) -> None:
        res_test_df, res_right_df = get_data_for_filter_test()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_data_for_merging_1(self) -> None:
        res_test_df, res_right_df = get_data_for_merging_test_1()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_data_for_merging_2(self) -> None:
        res_test_df, res_right_df = get_data_for_merging_test_2()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_data_for_merging_3(self) -> None:
        res_test_df, res_right_df = get_data_for_merging_test_3()
        self.assertTrue(is_equals(res_test_df, res_right_df))
