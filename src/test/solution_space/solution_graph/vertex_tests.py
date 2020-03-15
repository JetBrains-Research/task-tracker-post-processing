import logging
import unittest

from src.main.solution_space.data_classes import User
from src.main.solution_space.solution_graph import Vertex
from src.main.util.consts import LOGGER_FORMAT, LOGGER_TEST_FILE


class TestVertex(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_adding_parent(self):
        child = Vertex()
        parents_len = 100
        parents = [Vertex() for _ in range(parents_len)]
        for parent in parents:
            child.add_parent(parent)
            self.assertEqual(parent.children, [child])
        self.assertEqual(child.parents, parents)

    def test_adding_children(self):
        parent = Vertex()
        children_len = 100
        children = [Vertex() for _ in range(children_len)]
        for child in children:
            parent.add_child(child)
            self.assertEqual(child.parents, [parent])
        self.assertEqual(parent.children, children)

    def test_adding_user(self):
        vertex = Vertex()
        users_len = 100
        users = [User() for _ in range(users_len)]
        for user in users:
            vertex.add_user(user)
        self.assertEqual(vertex.users, users)

