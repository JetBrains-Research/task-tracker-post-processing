# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import List, Optional

from src.main.solution_space.solution_graph import Vertex
from src.main.solution_space.path_finder_test_system import skip
from src.main.solution_space.path_finder.path_finder import IPathFinder, log
from src.main.canonicalization.canonicalization import get_code_from_tree, are_asts_equal
from src.main.solution_space.consts import DISTANCE_TO_GRAPH_THRESHOLD, DIFFS_PERCENT_TO_GO_DIRECTLY


@skip(reason='We removed dist between vertices in the graph because it worked too slow, but this version uses it')
class PathFinderV1(IPathFinder):

    def find_next_anon_tree(self, user_vertex: Vertex) -> Vertex:
        """
        1. Find the closest goal (__find_closest_goal)
        2. Find the closest graph_vertex (__find_closest_vertex_with_path)
        3. Choose between them using __go_through_graph
        """

        log.info(f'{self.__class__.__name__}\n'
                 f'Start finding the next code state for '
                 f'the user code:\n{get_code_from_tree(user_vertex.serialized_code.anon_trees[0])}\nand '
                 f'the user:\n{user_vertex.code_info_list[0].user}')
        goal = self.__find_closest_goal(user_vertex)
        log.info(f'Chosen goal is vertex {goal.id}')
        graph_vertex = self.__find_closest_vertex(user_vertex, goal)
        log.info(f'Chosen graph_vertex is vertex {graph_vertex.id}')
        # We can have graph_vertex = None
        if graph_vertex and self.__go_through_graph(user_vertex, graph_vertex, goal):
            log.info(f'We are going through graph')
            return graph_vertex
        else:
            log.info(f'We are going directly to the goal')
            return goal

    def __choose_best_vertex(self, user_vertex: Vertex, vertices: List[Vertex]) -> Optional[Vertex]:
        """
        1. Sort candidates using MeasuredVertex
        2. Return the first candidate
        """
        log.info(f'Number of candidates: {len(vertices)}\nCandidates ids are {([vertex.id for vertex in vertices])}')
        if len(vertices) == 0:
            return None
        candidates = list(map(lambda vertex: self.get_measured_tree(user_vertex, vertex), vertices))
        candidates.sort()
        log.info(f'The best vertex id is {candidates[0].vertex.id}')
        return candidates[0].vertex

    # Note: A goal is a vertex, which has the rate equals 1 and it connects to the end vertex
    def __find_closest_goal(self, user_vertex: Vertex) -> Vertex:
        """
        1. Get list of all goals
        2. Find the closest using __choose_best_vertex()
        """
        goals = self._graph.end_vertex.parents
        log.info(f'Number of goals: {len(goals)}\nGoals ids are {[g.id for g in goals]}')
        return self.__choose_best_vertex(user_vertex, goals)

    # Note: we have to remove the 'user_code' from the set
    def __find_closest_vertex(self, user_vertex: Vertex, goal: Vertex,
                              to_add_empty: bool = False) -> Optional[Vertex]:
        """
        1. For each (by default, not empty) vertex with different canon_tree:
            1.1 Find dist from it to goal
            1.2 Consider as candidate if dist <= user_dist_to_goal
        2. Choose the best vertex from candidates using __choose_best_vertex()
        """
        user_diffs_to_goal = goal.get_dist(user_vertex)
        log.info(f'User diff to goal is {user_diffs_to_goal}')
        candidates = []
        for vertex in self._graph.get_traversal():
            # We don't want to add to result the same vertex
            if are_asts_equal(user_vertex.serialized_code.canon_tree, vertex.serialized_code.canon_tree):
                continue
            if not to_add_empty and self._graph.is_empty_vertex(vertex):
                continue

            # Todo: calculate diffs to the nearest goal from each vertex or not???
            # Todo: think about empty tree
            diffs = self._graph.get_dist_between_vertices(vertex, goal)

            if diffs <= user_diffs_to_goal:
                candidates.append(vertex)
        return self.__choose_best_vertex(user_vertex, candidates)

    @staticmethod
    def __is_far_from_graph(diffs_from_user_to_goal: int, diffs_from_user_to_graph_vertex: int) -> bool:
        return diffs_from_user_to_graph_vertex / diffs_from_user_to_goal > DISTANCE_TO_GRAPH_THRESHOLD

    @staticmethod
    def __is_most_of_path_is_done(diffs_from_empty_to_goal: int, diffs_from_user_to_goal: int) -> bool:
        return diffs_from_user_to_goal <= diffs_from_empty_to_goal * DIFFS_PERCENT_TO_GO_DIRECTLY

    # Returns should we go through graph or directly to the goal
    def __go_through_graph(self, user_vertex: Vertex, graph_vertex: Vertex, goal: Vertex) -> bool:
        """
        1. If __is_most_of_path_is_done, return False
        2. Return not __is_far_from_graph
        """
        diffs_from_user_to_goal = user_vertex.get_dist(goal)
        diffs_from_empty_to_user = self._graph.empty_vertex.get_dist(user_vertex)
        if self.__is_most_of_path_is_done(diffs_from_empty_to_user + diffs_from_user_to_goal,
                                          diffs_from_user_to_goal):
            log.info('Most of path is done')
            return False

        diffs_from_user_to_graph_vertex = user_vertex.get_dist(graph_vertex)
        return not self.__is_far_from_graph(diffs_from_user_to_goal, diffs_from_user_to_graph_vertex)
