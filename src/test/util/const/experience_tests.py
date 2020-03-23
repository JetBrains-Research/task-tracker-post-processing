# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import unittest

from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT, EXPERIENCE, DEFAULT_VALUES


class TestExperienceMethods(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_value_error_experience(self):
        self.assertRaises(ValueError, EXPERIENCE.__lt__, EXPERIENCE.LESS_THAN_HALF_YEAR,  5)

    def test_equal_experience(self):
        self.assertFalse(EXPERIENCE.LESS_THAN_HALF_YEAR < EXPERIENCE.LESS_THAN_HALF_YEAR)

    def test_less_experience(self):
        self.assertTrue(EXPERIENCE.LESS_THAN_HALF_YEAR < EXPERIENCE.MORE_THAN_SIX)

    def test_more_experience(self):
        self.assertFalse(EXPERIENCE.MORE_THAN_SIX < EXPERIENCE.LESS_THAN_HALF_YEAR)

    def test_default_experience_1(self):
        self.assertFalse(EXPERIENCE.LESS_THAN_HALF_YEAR < DEFAULT_VALUES.EXPERIENCE)

    def test_default_experience_2(self):
        self.assertTrue(DEFAULT_VALUES.EXPERIENCE < EXPERIENCE.LESS_THAN_HALF_YEAR)

    def test_two_default_experiences(self):
        self.assertFalse(DEFAULT_VALUES.EXPERIENCE.__lt__(DEFAULT_VALUES.EXPERIENCE))
