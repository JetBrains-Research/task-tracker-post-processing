import logging
import unittest

from src.main.solution_space.data_classes import User
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_user_id(self):
        n = 100
        for i in range(n):
            user = User()
            self.assertEqual(user.id, i)