from typing import List, Optional

from src.main.canonicalization.canonicalization import get_code_from_tree, are_asts_equal
from src.main.canonicalization.diffs.diff_handler import IDiffHandler
from src.main.solution_space.consts import DISTANCE_TO_GRAPH_THRESHOLD, DIFFS_PERCENT_TO_GO_DIRECTLY, EMPTY_DIFF_HANDLER
from src.main.solution_space.data_classes import User
from src.main.solution_space.path_finder.path_finder import IPathFinder, log, MeasuredVertex
from src.main.solution_space.vertex import Vertex

"""
The first version of path finder.
*an algorithm description goes here*
"""
# Todo: add description as a field

class PathFinderV1(IPathFinder):

    def find_next_vertex(self, user_diff_handler: IDiffHandler, user: User) -> Vertex:
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
    def __choose_best_vertex(user_diff_handler: IDiffHandler, user: User, vertices: List[Vertex]) -> Optional[Vertex]:
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
                                        goal: Vertex, to_add_empty: bool = False) -> Optional[Vertex]:
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
                    and get_code_from_tree(vertex.code.anon_tree[0]) == '' \
                    and not to_add_empty:
                continue

            # Todo: calculate diffs to the nearest goal from each vertex or not???
            # Todo: think about empty tree
            diffs = self._graph.get_dist_between_vertices(vertex, goal)

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
    def __go_through_graph(user_diff_handler: IDiffHandler, graph_vertex: Vertex, goal: Vertex) -> bool:

        diffs_from_user_to_goal = goal.get_diffs_number_to_vertex(user_diff_handler)
        diffs_from_empty_to_user = user_diff_handler.get_diffs_number_from_diff_handler(EMPTY_DIFF_HANDLER)
        if PathFinderV1.__is_most_of_path_is_done(diffs_from_empty_to_user + diffs_from_user_to_goal,
                                                  diffs_from_user_to_goal):
            return False

        diffs_from_user_to_graph_vertex = graph_vertex.get_diffs_number_to_vertex(user_diff_handler)
        return not PathFinderV1.__is_far_from_graph(diffs_from_user_to_goal, diffs_from_user_to_graph_vertex)