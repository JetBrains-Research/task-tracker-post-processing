# Copyright (c) by anonymous author(s)

import pytest

from src.main.util.consts import TASK
from src.test.test_config import to_skip, TEST_LEVEL
from src.main.solution_space.data_classes import User, CodeInfo
from src.main.solution_space.consts import SOLUTION_SPACE_TEST_FOLDER
from src.main.solution_space.solution_graph import Vertex, SolutionGraph

CURRENT_TASK = TASK.PIES
SolutionGraph.solution_space_folder = SOLUTION_SPACE_TEST_FOLDER


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestVertex:

    def test_adding_parent(self) -> None:
        sg = SolutionGraph(CURRENT_TASK)
        child = Vertex(sg)
        parents_len = 100
        parents = [Vertex(sg) for _ in range(parents_len)]
        for parent in parents:
            child.add_parent(parent)
            assert parent.children == [child]
        assert child.parents == parents

    def test_adding_children(self) -> None:
        sg = SolutionGraph(CURRENT_TASK)
        parent = Vertex(sg)
        children_len = 100
        children = [Vertex(sg) for _ in range(children_len)]
        for child in children:
            parent.add_child(child)
            assert child.parents == [parent]
        assert parent.children == children

    @pytest.mark.skip(reason='There is no code info in the vertex now')
    def test_adding_code_info(self) -> None:
        sg = SolutionGraph(CURRENT_TASK)
        vertex = Vertex(sg)
        code_info_list_len = 100
        code_info_list = [CodeInfo(User()) for _ in range(code_info_list_len)]
        for code_info in code_info_list:
            vertex.add_code_info(code_info)
        assert vertex.code_info_list == code_info_list

    @pytest.mark.skip(reason='There is no code info in the vertex now')
    def test_getting_unique_users(self) -> None:
        users = [User(), User(), User()]
        users_dist = [3, 0, 20]
        code_info_list = []
        # Create code_info_list with users distribution
        for i, dist in enumerate(users_dist):
            for j in range(dist):
                code_info_list.append(CodeInfo(users[i]))
        assert len(code_info_list) == sum(users_dist)

        sg = SolutionGraph(CURRENT_TASK)
        vertex = Vertex(sg)
        for code_info in code_info_list:
            vertex.add_code_info(code_info)

        # In result set will be only two users form three because the second one has 0 code_info
        assert vertex.get_unique_users() == {users[0], users[2]}
