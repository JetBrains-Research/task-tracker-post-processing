import unittest

from src.main.util.log_util import configure_logger


class LoggedTest(unittest.TestCase):
    def setUp(self) -> None:
        configure_logger(in_test_mode=True)
