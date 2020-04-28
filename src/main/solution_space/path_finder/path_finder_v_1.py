# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging
from typing import List, Optional

from src.main.solution_space.data_classes import User
from src.main.solution_space.measured_vertex.measured_vertex import MeasuredVertex
from src.main.solution_space.path_finder.path_finder import IPathFinder
from src.main.solution_space.solution_graph import Vertex
from src.main.canonicalization.diffs.diff_handler import IDiffHandler
from src.main.canonicalization.diffs.gumtree_diff_handler import GumTreeDiffHandler
from src.main.util import consts
from src.main.util.consts import LOGGER_NAME
from src.main.util.log_util import log_and_raise_error
from src.main.canonicalization.diffs.rivers_diff_handler import RiversDiffHandler
from src.main.solution_space.data_classes import User, Profile
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.canonicalization.canonicalization import are_asts_equal, get_trees, get_code_from_tree
from src.main.solution_space.consts import DIFFS_PERCENT_TO_GO_DIRECTLY, DISTANCE_TO_GRAPH_THRESHOLD, EMPTY_DIFF_HANDLER

log = logging.getLogger(LOGGER_NAME)


class PathFinderV3(IPathFinder):

    _description: str = \
        """
        PathFinder
        version: 1
        find_next_vertex: *description*
        choose_best_vertex: *description*
        """

    @classmethod
    def description(cls) -> str:
        return cls._description

    # Find a next canonicalized code state
    # Todo: 14/04 calculate user rate
    def find_next_vertex(self, user_diff_handler: IDiffHandler, user: User, user_rate: float) -> Vertex:
        # Todo: check if user_code is not valid
        # Todo: add method for getting source_code to DiffHandler?
        log.info(f'Start finding the next code state for the user code: '
                 f'{get_code_from_tree(user_diff_handler.orig_tree)} and the user: {user}')
        # Todo: what to do if goal is None?
        goal = self.__find_closest_goal(user_diff_handler, user)
        graph_vertex = self.__find_closest_vertex_with_path(user_diff_handler, user, goal)
        # We can have graph_vertex = None
        if graph_vertex and self.__go_through_graph(user_diff_handler, graph_vertex, goal, user_rate=user_rate):
            log.info(f'We are going through graph')
            return graph_vertex
        else:
            log.info(f'We are going directly to the goal')
            return goal

    # Sort candidates and return the best for user_code from ones
    @staticmethod
    def __choose_best_vertex(user_diff_handler: IDiffHandler, user: User,
                             vertices: List[Vertex]) -> Optional[Vertex]:
        if len(vertices) == 0:
            return None
        candidates = list(map(lambda vertex: MeasuredVertex(user_diff_handler, vertex, user), vertices))
        candidates.sort()
        log.info(f'Candidates ids are {([c.vertex.id for c in candidates])}')
        log.info(f'The best vertex id is {candidates[0].vertex.id}')
        return candidates[0].vertex

    # Use '__choose_best_vertex' for choosing the best goal from all ones
    # Note: A goal is a vertex, which has the rate equals 1 and it connects to the end vertex
    def __find_closest_goal(self, user_diff_handler: IDiffHandler, user: User) -> Vertex:
        log.info(f'Goals ids are {[p.id for p in self._graph.end_vertex.parents]}')
        return self.__choose_best_vertex(user_diff_handler, user, self._graph.end_vertex.parents)

    # Calculate a set of vertices, which contains all vertices
    # that have a distance (number of diffs) to the goal <= than 'user_code'
    # Run __choose_best_vertex on these vertices, which returns None in case of the empty list
    # Note: we have to remove the 'user_code' from the set
    def __find_closest_vertex_with_path(self, user_diff_handler: IDiffHandler, user: User,
                                        goal: Vertex) -> Optional[Vertex]:
        # Todo: move somewhere as a separate method
        user_diffs_to_goal = goal.get_diffs_number_to_vertex(user_diff_handler)

        # Todo: 14/04 test vertex from graph
        vertex_in_graph = self._graph.find_vertex_by_canon_tree(user_diff_handler.canon_tree)
        if vertex_in_graph:
            return self.__choose_best_vertex(user_diff_handler, user, vertex_in_graph.children)

        candidates = []
        vertices = self._graph.get_traversal()
        vertices.remove(self._graph.start_vertex)

        for vertex in vertices:
            # Todo: use const for 0.7
            if self.__class__\
                    .__get_is_rollback_probability(user_diff_handler.canon_tree, vertex.code.canon_tree) <= 0.7:
                candidates.append(vertex)
            #
            # diffs = self._graph.get_diffs_number_between_vertexes(vertex, goal)
            #
            # if diffs <= user_diffs_to_goal:
            #     candidates.append(vertex)
        return self.__choose_best_vertex(user_diff_handler, user, candidates)

    @staticmethod
    def __get_is_rollback_probability(user_canon_tree: ast.AST, vertex_canon_tree: ast.AST) -> float:
        # Todo: use AST comparing or other measure
        included_lines_count = 0
        vertex_code_lines = get_code_from_tree(vertex_canon_tree).strip('\n').split('\n')
        user_code = get_code_from_tree(user_canon_tree)
        for line in vertex_code_lines:
            if line in user_code:
                included_lines_count += 1
        return included_lines_count / len(vertex_code_lines)

    @staticmethod
    def __is_far_from_graph(diffs_from_user_to_goal: int, diffs_from_user_to_graph_vertex: int) -> bool:
        return diffs_from_user_to_graph_vertex / diffs_from_user_to_goal > DISTANCE_TO_GRAPH_THRESHOLD

    @staticmethod
    def __is_most_of_path_is_done(diffs_from_empty_to_goal: int, diffs_from_user_to_goal: int) -> bool:
        return diffs_from_user_to_goal <= diffs_from_empty_to_goal * DIFFS_PERCENT_TO_GO_DIRECTLY

    @staticmethod
    def __is_rate_worse(user_rate: float, graph_vertex_rate: float):
        # TODO: 14/04 or If number of passed tests > 0 then True???
        return user_rate > 0 and graph_vertex_rate == 0

    # Choose the best way to go to the goal
    # For example, if we have a good way through the graph, we should advise it,
    # but if don't we would advise going directly to the goal
    @staticmethod
    def __go_through_graph(user_diff_handler: IDiffHandler, graph_vertex: Vertex, goal: Vertex,
                           user_rate: float = 0.0) -> bool:
        diffs_from_user_to_goal = goal.get_diffs_number_to_vertex(user_diff_handler)
        diffs_from_empty_to_user = user_diff_handler.get_diffs_number_from_diff_handler(EMPTY_DIFF_HANDLER)

        if PathFinderV3.__is_most_of_path_is_done(diffs_from_empty_to_user + diffs_from_user_to_goal,
                                                  diffs_from_user_to_goal):
            return False

        if PathFinderV3.__is_rate_worse(user_rate, graph_vertex.code.rate):
            return False

        diffs_from_user_to_graph_vertex = graph_vertex.get_diffs_number_to_vertex(user_diff_handler)
        return not PathFinderV3.__is_far_from_graph(diffs_from_user_to_goal, diffs_from_user_to_graph_vertex)
