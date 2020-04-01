# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.util.consts import TASK
from src.test.test_util import LoggedTest
from src.main.solution_space.data_classes import User, CodeInfo
from src.main.solution_space.solution_graph import Vertex, SolutionGraph
from src.main.solution_space.consts import FOLDER_WITH_CODE_FILES_FOR_TESTS

CURRENT_TASK = TASK.PIES
SolutionGraph.folder_with_code_files = FOLDER_WITH_CODE_FILES_FOR_TESTS


class TestVertex(LoggedTest):

    def test_adding_parent(self) -> None:
        sg = SolutionGraph(CURRENT_TASK)
        child = Vertex(sg)
        parents_len = 100
        parents = [Vertex(sg) for _ in range(parents_len)]
        for parent in parents:
            child.add_parent(parent)
            self.assertEqual(parent.children, [child])
        self.assertEqual(child.parents, parents)

    def test_adding_children(self) -> None:
        sg = SolutionGraph(CURRENT_TASK)
        parent = Vertex(sg)
        children_len = 100
        children = [Vertex(sg) for _ in range(children_len)]
        for child in children:
            parent.add_child(child)
            self.assertEqual(child.parents, [parent])
        self.assertEqual(parent.children, children)

    def test_adding_code_info(self) -> None:
        sg = SolutionGraph(CURRENT_TASK)
        vertex = Vertex(sg)
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

        sg = SolutionGraph(CURRENT_TASK)
        vertex = Vertex(sg)
        for code_info in code_info_list:
            vertex.add_code_info(code_info)

        # In result set will be only two users form three because the second one has 0 code_info
        self.assertEqual(vertex.get_unique_users(), {users[0], users[2]})
