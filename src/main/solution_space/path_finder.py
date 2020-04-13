# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import List, Optional

from src.main.util import consts
from src.main.util.log_util import log_and_raise_error
from src.main.canonicalization.consts import TREE_TYPE
from src.main.canonicalization.diffs.rivers_diff_handler import RiversDiffHandler
from src.main.solution_space.data_classes import Code, User, Profile
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.canonicalization.canonicalization import are_asts_equal, get_trees, get_code_from_tree
from src.main.solution_space.consts import DIFFS_PERCENT_TO_GO_DIRECTLY, DISTANCE_TO_GRAPH_THRESHOLD, EMPTY_DIFF_HANDLER

log = logging.getLogger(consts.LOGGER_NAME)


class PathFinder:
    def __init__(self, graph: SolutionGraph):
        self._graph = graph

    @property
    def graph(self) -> SolutionGraph:
        return self._graph

    # Find a next canonicalized code state
    def find_next_vertex(self, user_diff_handler: RiversDiffHandler, user: User) -> Vertex:
        # Todo: check if user_code is not valid
        # Todo: add method for getting source_code to DiffHandler?
        log.info(f'Start finding the next code state for the user code: '
                 f'{get_code_from_tree(user_diff_handler.orig_tree)} and the user: {user}')
        # Todo: what to do if goal is None?
        goal = self.__find_closest_goal(user_diff_handler, user)
        graph_vertex = self.__find_closest_vertex_with_path(user_diff_handler, user, goal)
        # We can have graph_vertex = None
        if graph_vertex and self.__go_through_graph(user_diff_handler, graph_vertex, goal):
            log.info(f'We are going through graph')
            return graph_vertex
        else:
            log.info(f'We are going directly to the goal')
            return goal

    # Sort candidates and return the best for user_code from ones
    @staticmethod
    def __choose_best_vertex(user_diff_handler: RiversDiffHandler, user: User, vertices: List[Vertex]) -> Optional[Vertex]:
        if len(vertices) == 0:
            return None
        candidates = list(map(lambda vertex: MeasuredVertex(user_diff_handler, vertex, user), vertices))
        candidates.sort()
        log.info(f'Candidates ids are {([c.vertex.id for c in candidates])}')
        log.info(f'The best vertex id is {candidates[-1].vertex.id}')
        return candidates[-1].vertex

    # Use '__choose_best_vertex' for choosing the best goal from all ones
    # Note: A goal is a vertex, which has the rate equals 1 and it connects to the end vertex
    def __find_closest_goal(self, user_diff_handler: RiversDiffHandler, user: User) -> Vertex:
        log.info(f'Goals ids are {[p.id for p in self._graph.end_vertex.parents]}')
        return self.__choose_best_vertex(user_diff_handler, user, self._graph.end_vertex.parents)

    # Calculate a set of vertices, which contains all vertices
    # that have a distance (number of diffs) to the goal <= than 'user_code'
    # Run __choose_best_vertex on these vertices, which returns None in case of the empty list
    # Note: we have to remove the 'user_code' from the set
    def __find_closest_vertex_with_path(self, user_diff_handler: RiversDiffHandler, user: User,
                                        goal: Vertex, to_add_empty: bool = False) -> Optional[Vertex]:
        # Todo: move somewhere as a separate method
        user_diffs_to_goal = goal.get_diffs_number_to_vertex(user_diff_handler)
        candidates = []
        vertices = self._graph.get_traversal()
        vertices.remove(self._graph.start_vertex)

        for vertex in vertices:
            # We don't want to add to result the same vertex
            if are_asts_equal(user_diff_handler.canon_tree, vertex.code.canon_tree):
                continue
            # Todo: change to normal way
            if get_code_from_tree(vertex.code.canon_tree) == '' \
                    and get_code_from_tree(vertex.code.anon_trees[0]) == '' \
                    and not to_add_empty:
                continue

            # Todo: calculate diffs to the nearest goal from each vertex or not???
            # Todo: think about empty tree
            diffs = self._graph.get_diffs_number_between_vertexes(vertex, goal)

            if diffs <= user_diffs_to_goal:
                candidates.append(vertex)
        return self.__choose_best_vertex(user_diff_handler, user, candidates)

    @staticmethod
    def __is_far_from_graph(diffs_from_user_to_goal: int, diffs_from_user_to_graph_vertex: int) -> bool:
        return diffs_from_user_to_graph_vertex / diffs_from_user_to_goal > DISTANCE_TO_GRAPH_THRESHOLD

    @staticmethod
    def __is_most_of_path_is_done(diffs_from_empty_to_goal: int, diffs_from_user_to_goal: int) -> bool:
        return diffs_from_user_to_goal <= diffs_from_empty_to_goal * DIFFS_PERCENT_TO_GO_DIRECTLY

    # Choose the best way to go to the goal
    # For example, if we have a good way through the graph, we should advise it,
    # but if don't we would advise going directly to the goal
    @staticmethod
    def __go_through_graph(user_diff_handler: RiversDiffHandler, graph_vertex: Vertex, goal: Vertex) -> bool:

        diffs_from_user_to_goal = goal.get_diffs_number_to_vertex(user_diff_handler)
        diffs_from_empty_to_user = len(user_diff_handler.get_diffs_from_diff_handler(EMPTY_DIFF_HANDLER)[0])
        if PathFinder.__is_most_of_path_is_done(diffs_from_empty_to_user + diffs_from_user_to_goal,
                                                diffs_from_user_to_goal):
            return False

        diffs_from_user_to_graph_vertex = graph_vertex.get_diffs_number_to_vertex(user_diff_handler)
        return not PathFinder.__is_far_from_graph(diffs_from_user_to_goal, diffs_from_user_to_graph_vertex)


class MeasuredVertex:
    def __init__(self, user_diff_handler: RiversDiffHandler, vertex: Vertex, user: User, distance: Optional[int] = None):
        self._vertex = vertex
        self._distance = distance if distance else vertex.get_diffs_number_to_vertex(user_diff_handler)
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
        return Profile()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, MeasuredVertex):
            return False
        if self._distance != o.distance or self._profile == o.profile:
            return False
        return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __lt__(self, o: object):
        if not isinstance(o, MeasuredVertex):
            log_and_raise_error(f'The object {o} is not {self.__class__} class', log)
        if self._distance < o.distance:
            return True
        # Todo: use profile info
        return self._users_count < o.users_count



