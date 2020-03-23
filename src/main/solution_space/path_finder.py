# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

from src.main.solution_space.consts import DIFFS_PERCENT_GO_THROUGH_GRAPH
from src.main.util import consts
from typing import List, Optional, Any
from src.main.util.consts import DEFAULT_VALUES
from src.main.solution_space.data_classes import Code, User, Profile
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.gum_tree_diff.gum_tree_diff import get_diffs_number, apply_diffs
from src.main.canonicalization.canonicalization import are_asts_equal, get_canonicalized_form
from src.main.util.statistics_util import calculate_safety_median, calculate_median_for_objects

log = logging.getLogger(consts.LOGGER_NAME)


class PathFinder:
    def __init__(self, graph: SolutionGraph):
        self._graph = graph
        self._median_age, self._median_experience = graph.calculate_median_of_profile_info()

    @property
    def graph(self) -> SolutionGraph:
        return self._graph

    @property
    def median_age(self) -> int:
        return self._median_age

    @property
    def median_experience(self) -> Any:
        return self._median_experience

    # Find a next canonicalization state for user code
    def find_next_code_state(self, user_code: Code, user: User) -> Code:
        # Todo: check if user_code is not valid
        log.info(f'Start finding the next code state for the user code: {user_code} and the user: {user}')
        goal = self.__find_closest_goal(user_code, user)
        median_of_diff_number_to_goal = self._graph.calculate_median_of_diff_number_to_goal(goal)
        log.info(f'The goal for the user code: {user_code} is\n{goal}\n'
                 f'Median of diff number is {median_of_diff_number_to_goal}')
        graph_vertex = self.__find_closest_vertex_with_path(user_code, user, goal)
        # We can have graph_vertex = None
        if graph_vertex and self.__go_through_graph(user_code, graph_vertex, goal, median_of_diff_number_to_goal):
            log.info(f'We are going through graph')
            next_code = self.__apply_minimal_actions_number(user_code, graph_vertex.code)
        else:
            log.info(f'We are going directly to the goal')
            next_code = self.__apply_minimal_actions_number(user_code, goal.code)
        log.info(f'Finish finding the next code state. The user: {user}\nThe user code: {user_code}\n'
                 f'The next code: {next_code}')
        return next_code

    # Sort candidates and return the best for user_code from ones
    @staticmethod
    def __choose_best_vertex(user_code: Code, user: User, vertices: List[Vertex]) -> Optional[Vertex]:
        if len(vertices) == 0:
            return None
        candidates = list(map(lambda vertex: Candidate(user_code, vertex, user), vertices))
        candidates.sort()
        return candidates[-1].vertex

    # Use '__choose_best_vertex' for choose the best goal from all ones
    # Note: A goal is a vertex, which has the rate equals 1 and it connects to the end vertex
    def __find_closest_goal(self, user_code: Code, user: User) -> Vertex:
        return self.__choose_best_vertex(user_code, user, self._graph.end_vertex.parents)

    # Calculate a set of vertices, which contains all vertices
    # that have a distance to the goal <= than 'user_code' (number of diffs)
    # Return None, if the size of the set is zero, otherwise run '__choose_best_vertex'
    # Note: we have to remove the 'user_code' from the set
    def __find_closest_vertex_with_path(self, user_code: Code, user: User, goal: Vertex) -> Optional[Vertex]:
        user_diffs_to_goal = get_diffs_number(user_code.file_with_code, goal.code.file_with_code)
        candidates = []
        vertices = self._graph.get_traversal()
        vertices.remove(self._graph.start_vertex)
        for vertex in vertices:
            # We don't want to add to result the same vertex
            if are_asts_equal(user_code.ast, vertex.code.ast):
                continue
            diffs = get_diffs_number(vertex.code.file_with_code, goal.code.file_with_code)
            if diffs <= user_diffs_to_goal:
                candidates.append(vertex)
        return self.__choose_best_vertex(user_code, user, vertices)

    # Choose the best way to go to the goal
    # For example, if we have a good way through the graph, we should advise it,
    # but if don't we would advise going directly to the goal
    @staticmethod
    def __go_through_graph(user_code: Code, graph_vertex: Vertex, goal: Vertex,
                           median_of_diff_number_to_goal: int) -> bool:
        # Todo: use graph_vertex too
        diffs_to_goal = get_diffs_number(user_code.file_with_code, goal.code.file_with_code)
        border_go_through_graph = median_of_diff_number_to_goal * (1 - DIFFS_PERCENT_GO_THROUGH_GRAPH)
        if diffs_to_goal <= border_go_through_graph:
            return False
        return True

    # Call gumTreeDiff methods
    @staticmethod
    def __apply_minimal_actions_number(user_code: Code, dst_code: Code) -> Code:
        str_code = apply_diffs(user_code.file_with_code, dst_code.file_with_code)
        ast = get_canonicalized_form(str_code)
        # Todo: get rate
        return Code(ast)


# Todo: rename it???
class Candidate:
    def __init__(self, user_code: Code, vertex: Vertex, user: User, distance: Optional[int] = None):
        self._vertex = vertex
        self._distance = distance if distance \
            else get_diffs_number(user_code.file_with_code, vertex.code.file_with_code)
        # Todo: get actual vertex profile
        self._profile = self.__init_profile(user)
        self._users_count = len(vertex.get_unique_users())

    @property
    def vertex(self) -> Vertex:
        return self._vertex

    @property
    def distance(self) -> int:
        return self._distance

    @property
    def profile(self) -> Profile:
        return self._profile

    @property
    def users_count(self) -> int:
        return self._users_count

    def __init_profile(self, user: User) -> Profile:
        # Todo: add user handling
        ages, experiences = [], []
        SolutionGraph.update_ages_and_experiences(self._vertex.code_info_list, ages, experiences)
        return Profile(calculate_safety_median(ages, default_value=DEFAULT_VALUES.AGE.value),
                       calculate_median_for_objects(experiences, default_value=DEFAULT_VALUES.EXPERIENCE))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Candidate):
            return False
        if self._distance != o.distance or self._profile == o.profile:
            return False
        return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __lt__(self, o: object):
        if not isinstance(o, Candidate):
            log.error(f'The object {o} is not {self.__class__} class')
            raise ValueError(f'The object {o} is not {self.__class__} class')
        if self._distance < o.distance:
            return True
        # Todo: use profile info
        # if self.profile.experience < o.profile.experience:
        #     return True
        # if self.profile.age < o.profile.age:
        #     return True
        return self._users_count < o.users_count



