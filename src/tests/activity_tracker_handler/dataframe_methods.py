from src import activity_tracker_handler as ath
import pandas as pd
import unittest

right_df = pd.DataFrame({'Number': [10, 11, 12, 13, 14], 'Key': ['A', 'B', 'C', 'D', 'E']})


def get_data_for_insert_by_index_test():
    test_df = pd.DataFrame({'Number': [10, 12, 13, 14],
                            'Key': ['A', 'C', 'D', 'E']})
    new_row_number = 1
    new_row_value = [11, 'B']
    res_test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    return res_test_df, right_df


def get_data_for_insert_two_times():
    test_df = pd.DataFrame({'Number': [10, 12, 14],
                            'Key': ['A', 'C', 'E']})
    new_row_number = 1
    new_row_value = [11, 'B']
    test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    new_row_number = 3
    new_row_value = [13, 'D']
    res_test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    return res_test_df, right_df


def get_data_for_insert_at_the_beginning_test():
    test_df = pd.DataFrame({'Number': [11, 12, 13, 14],
                            'Key': ['B', 'C', 'D', 'E']})
    new_row_number = 0
    new_row_value = [10, 'A']
    res_test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    return res_test_df, right_df


def get_data_for_insert_at_the_end_test():
    test_df = pd.DataFrame({'Number': [10, 11, 12, 13],
                            'Key': ['A', 'B', 'C', 'D']})
    new_row_number = 4
    new_row_value = [14, 'E']
    res_test_df = ath.__insert_row(test_df, new_row_number, new_row_value)
    return res_test_df, right_df


def is_equals(df_1: pd.DataFrame, df_2: pd.DataFrame):
    return df_1.equals(df_2)


class TestDataFrameMethods(unittest.TestCase):

    def test_insert_by_index(self):
        res_test_df, res_right_df = get_data_for_insert_by_index_test()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_data_for_insert_two_times(self):
        res_test_df, res_right_df = get_data_for_insert_two_times()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_data_for_insert_at_the_beginning_test(self):
        res_test_df, res_right_df = get_data_for_insert_at_the_beginning_test()
        self.assertTrue(is_equals(res_test_df, res_right_df))

    def test_data_for_insert_at_the_end_test(self):
        res_test_df, res_right_df = get_data_for_insert_at_the_end_test()
        self.assertTrue(is_equals(res_test_df, res_right_df))
