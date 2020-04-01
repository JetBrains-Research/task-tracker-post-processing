# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.test.test_util import LoggedTest
from src.main.solution_space.data_classes import User
from src.test.solution_space.solution_graph.util import init_default_ids


class TestUser(LoggedTest):

    def test_user_id(self) -> None:
        init_default_ids()
        n = 100
        for i in range(n):
            user = User()
            self.assertEqual(user.id, i)
