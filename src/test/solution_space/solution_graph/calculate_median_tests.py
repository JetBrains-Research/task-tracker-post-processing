# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import unittest

from typing import Tuple, Any
from src.main.solution_space.data_classes import Code, Profile, User, CodeInfo
from src.main.solution_space.solution_graph import SolutionGraph
from src.test.solution_space.solution_graph.util import get_two_vertices
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT, LOGGER_NAME, TASK, DEFAULT_VALUES, EXPERIENCE

log = logging.getLogger(LOGGER_NAME)


CURRENT_TASK = TASK.PIES
DEFAULT_PROFILE = Profile()
DEFAULT_USER = User(DEFAULT_PROFILE)


def init_graph() -> SolutionGraph:
    sg = SolutionGraph(CURRENT_TASK)
    vertices = get_two_vertices(sg)
    for v in vertices:
        sg.connect_to_start_vertex(v)
        sg.connect_to_end_vertex(v)
    return sg


SG = init_graph()


def compare_results(expected_age_and_exp: Tuple[int, Any],
                    actual_age_and_exp: Tuple[int, Any]) -> bool:
    expected_age, expected_exp = expected_age_and_exp
    actual_age, actual_exp = actual_age_and_exp
    return expected_age == actual_age and expected_exp == actual_exp


def add_user_to_all_vertices(user: User) -> None:
    vertices = SG.get_traversal()
    vertices.remove(SG.start_vertex)
    for vertex in vertices:
        vertex.add_code_info(CodeInfo(user))


def add_user_to_n_vertices(user: User, n: int = 2) -> None:
    vertices = SG.get_traversal()
    vertices.remove(SG.start_vertex)
    for vertex in vertices:
        n -= 1
        if n < 0:
            break
        vertex.add_code_info(CodeInfo(user))


class TestCalculateMedianMethods(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_empty_profiles(self):
        age, experience = SG.calculate_median_of_profile_info()
        self.assertTrue((DEFAULT_VALUES.AGE.value, DEFAULT_VALUES.EXPERIENCE), (age, experience))

    def test_default_profiles(self):
        add_user_to_all_vertices(DEFAULT_USER)
        age, experience = SG.calculate_median_of_profile_info()
        self.assertTrue((DEFAULT_VALUES.AGE.value, DEFAULT_VALUES.EXPERIENCE), (age, experience))

    def test_default_ages(self):
        profile_1 = Profile(experience=EXPERIENCE.FROM_FOUR_TO_SIX_YEARS)
        profile_2 = Profile(experience=EXPERIENCE.LESS_THAN_HALF_YEAR)
        add_user_to_all_vertices(User(profile_1))
        add_user_to_n_vertices(User(profile_2), 1)
        age, experience = SG.calculate_median_of_profile_info()
        self.assertTrue((DEFAULT_VALUES.AGE.value, EXPERIENCE.FROM_FOUR_TO_SIX_YEARS), (age, experience))

    def test_default_experience(self):
        profile_1 = Profile(age=15)
        profile_2 = Profile(age=21)
        add_user_to_all_vertices(User(profile_1))
        add_user_to_n_vertices(User(profile_2), 1)
        age, experience = SG.calculate_median_of_profile_info()
        self.assertTrue((15, DEFAULT_VALUES.EXPERIENCE), (age, experience))

    def test_same_ages_1(self):
        profile_1 = Profile(age=15)
        profile_2 = Profile(age=21)
        add_user_to_all_vertices(User(profile_1))
        add_user_to_all_vertices(User(profile_2))
        age, experience = SG.calculate_median_of_profile_info()
        self.assertTrue((15, EXPERIENCE.FROM_FOUR_TO_SIX_YEARS), (age, experience))

    def test_same_ages_2(self):
        profile_1 = Profile(age=15)
        profile_2 = Profile(age=21)
        add_user_to_all_vertices(User(profile_2))
        add_user_to_all_vertices(User(profile_1))
        age, experience = SG.calculate_median_of_profile_info()
        self.assertTrue((15, EXPERIENCE.FROM_FOUR_TO_SIX_YEARS), (age, experience))

    def test_same_experience_1(self):
        profile_1 = Profile(experience=EXPERIENCE.FROM_FOUR_TO_SIX_YEARS)
        profile_2 = Profile(experience=EXPERIENCE.LESS_THAN_HALF_YEAR)
        add_user_to_all_vertices(User(profile_1))
        add_user_to_all_vertices(User(profile_2))
        age, experience = SG.calculate_median_of_profile_info()
        self.assertTrue((DEFAULT_VALUES.AGE.value, EXPERIENCE.LESS_THAN_HALF_YEAR), (age, experience))

    def test_same_experience_2(self):
        profile_1 = Profile(experience=EXPERIENCE.FROM_FOUR_TO_SIX_YEARS)
        profile_2 = Profile(experience=EXPERIENCE.LESS_THAN_HALF_YEAR)
        add_user_to_all_vertices(User(profile_2))
        add_user_to_all_vertices(User(profile_1))
        age, experience = SG.calculate_median_of_profile_info()
        self.assertTrue((DEFAULT_VALUES.AGE.value, EXPERIENCE.LESS_THAN_HALF_YEAR), (age, experience))



