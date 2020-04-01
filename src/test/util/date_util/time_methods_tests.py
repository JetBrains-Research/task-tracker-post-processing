# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.test.test_util import LoggedTest
from src.main.util.time_util import corrected_time


def get_res_for_corrected_positive_time_test() -> bool:
    return corrected_time('2019-12-09T18:41:28.548+03:00') == '2019-12-09T18:41:28.548+0300'


def get_res_for_corrected_negative_time_test() -> bool:
    return corrected_time('2019-12-09T18:41:28.548-03:00') == '2019-12-09T18:41:28.548-0300'


class TestTimeMethods(LoggedTest):

    def test_corrected_positive_time(self) -> None:
        self.assertTrue(get_res_for_corrected_positive_time_test())

    def test_corrected_negative_time(self) -> None:
        self.assertTrue(get_res_for_corrected_negative_time_test())
