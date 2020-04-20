# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pytest

from src.test.util import to_skip, TEST_LEVEL
from src.main.solution_space.data_classes import User
from src.test.solution_space.solution_graph.util import init_default_ids


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestUser:

    @staticmethod
    def is_first_test(test_index: int) -> bool:
        return test_index == 0

    @pytest.mark.parametrize('i', range(100))
    def test_user_id(self, i: int) -> None:
        if self.__class__.is_first_test(i):
            # Before all tests
            init_default_ids()
        user = User()
        assert user.id == i
