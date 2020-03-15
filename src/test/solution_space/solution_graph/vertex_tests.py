import logging
import unittest

from src.main.solution_space.data_classes import User, CodeInfo
from src.main.solution_space.solution_graph import Vertex
from src.main.util.consts import LOGGER_FORMAT, LOGGER_TEST_FILE


class TestVertex(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_adding_parent(self) -> None:
        child = Vertex()
        parents_len = 100
        parents = [Vertex() for _ in range(parents_len)]
        for parent in parents:
            child.add_parent(parent)
            self.assertEqual(parent.children, [child])
        self.assertEqual(child.parents, parents)

    def test_adding_children(self) -> None:
        parent = Vertex()
        children_len = 100
        children = [Vertex() for _ in range(children_len)]
        for child in children:
            parent.add_child(child)
            self.assertEqual(child.parents, [parent])
        self.assertEqual(parent.children, children)

    def test_adding_code_info(self) -> None:
        vertex = Vertex()
        code_infos_len = 100
        code_infos = [CodeInfo(User()) for _ in range(code_infos_len)]
        for code_info in code_infos:
            vertex.add_code_info(code_info)
        self.assertEqual(vertex.code_infos, code_infos)

    def test_getting_unique_users(self) -> None:
        users = [User(), User(), User()]
        users_dist = [3, 0, 20]
        code_infos = []
        # create code_infos with users distribution
        for i, dist in enumerate(users_dist):
            for j in range(dist):
                code_infos.append(CodeInfo(users[i]))
        self.assertEqual(len(code_infos), sum(users_dist))

        vertex = Vertex()
        for code_info in code_infos:
            vertex.add_code_info(code_info)

        # in result set wiil be only two users form three because the second one has 0 code_infos
        self.assertEqual(vertex.get_unique_users(), {users[0], users[2]})

