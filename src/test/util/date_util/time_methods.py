import unittest

from src.main.util.date_util import corrected_time


def get_res_for_corrected_positive_time_test():
    return corrected_time('2019-12-09T18:41:28.548+03:00') == '2019-12-09T18:41:28.548+0300'


def get_res_for_corrected_negative_time_test():
    return corrected_time('2019-12-09T18:41:28.548-03:00') == '2019-12-09T18:41:28.548-0300'


class TestTimeMethods(unittest.TestCase):

    def test_corrected_positive_time(self):
        self.assertTrue(get_res_for_corrected_positive_time_test())

    def test_corrected_negative_time(self):
        self.assertTrue(get_res_for_corrected_negative_time_test())
