# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.util.consts import TASK
from src.test.test_util import LoggedTest
from src.main.solution_space.data_classes import User, CodeInfo
from src.main.solution_space.consts import SOLUTION_SPACE_TEST_FOLDER
from src.main.solution_space.solution_graph import SolutionGraph, Vertex

CURRENT_TASK = TASK.PIES
SolutionGraph.solution_space_folder = SOLUTION_SPACE_TEST_FOLDER


class TestVertex(LoggedTest):

    def test_adding_parent(self) -> None:
        graph = SolutionGraph(CURRENT_TASK)
        child = Vertex(graph)
        parents_len = 100
        parents = [Vertex(graph) for _ in range(parents_len)]
        for parent in parents:
            child.add_parent(parent)
            self.assertEqual(parent.children, [child])
        self.assertEqual(child.parents, parents)

    def test_adding_children(self) -> None:
        graph = SolutionGraph(CURRENT_TASK)
        parent = Vertex(graph)
        children_len = 100
        children = [Vertex(graph) for _ in range(children_len)]
        for child in children:
            parent.add_child(child)
            self.assertEqual(child.parents, [parent])
        self.assertEqual(parent.children, children)

    def test_adding_code_info(self) -> None:
        graph = SolutionGraph(CURRENT_TASK)
        vertex = Vertex(graph)
        code_info_list_len = 100
        code_info_list = [CodeInfo(User()) for _ in range(code_info_list_len)]
        for code_info in code_info_list:
            vertex.add_code_info(code_info)
        self.assertEqual(vertex.code_info_list, code_info_list)

    def test_getting_unique_users(self) -> None:
        users = [User(), User(), User()]
        users_dist = [3, 0, 20]
        code_info_list = []
        # Create code_info_list with users distribution
        for i, dist in enumerate(users_dist):
            for j in range(dist):
                code_info_list.append(CodeInfo(users[i]))
        self.assertEqual(len(code_info_list), sum(users_dist))

        graph = SolutionGraph(CURRENT_TASK)
        vertex = Vertex(graph)
        for code_info in code_info_list:
            vertex.add_code_info(code_info)

        # In result set will be only two users form three because the second one has 0 code_info
        self.assertEqual(vertex.get_unique_users(), {users[0], users[2]})
