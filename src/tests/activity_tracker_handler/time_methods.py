from src import activity_tracker_handler as ath
import unittest

# Todo: find the best way for testing the private methods
res_positive_time = ath.__corrected_time('2019-12-09T18:41:28.548+03:00')
res_negative_time = ath.__corrected_time('2019-12-09T18:41:28.548-03:00')


class TestTimeMethods(unittest.TestCase):

    def test_corrected_positive_time(self):
        self.assertEqual(res_positive_time, '2019-12-09T18:41:28.548+0300')

    def test_corrected_negative_time(self):
        self.assertEqual(res_negative_time, '2019-12-09T18:41:28.548-0300')




