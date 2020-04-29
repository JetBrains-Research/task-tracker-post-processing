# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import List, Optional

from src.main.solution_space.solution_graph import Vertex
from src.main.solution_space.path_finder.path_finder import IPathFinder, log
from src.main.canonicalization.canonicalization import get_code_from_tree, are_asts_equal
from src.main.solution_space.consts import DISTANCE_TO_GRAPH_THRESHOLD, DIFFS_PERCENT_TO_GO_DIRECTLY


class PathFinderV1(IPathFinder):

    def find_next_vertex(self, user_vertex: Vertex) -> Vertex:
        'description'
        log.info(f'Start finding the next code state for '
                 f'the user code: {get_code_from_tree(user_vertex.serialized_code.anon_trees[0])} and '
                 f'the user: {user_vertex.code_info_list[0].user}')
        goal = self.__find_closest_goal(user_vertex)
        graph_vertex = self.__find_closest_vertex_with_path(user_vertex, goal)
        # We can have graph_vertex = None
        if graph_vertex and self.__go_through_graph(user_vertex, graph_vertex, goal):
            log.info(f'We are going through graph')
            return graph_vertex
        else:
            log.info(f'We are going directly to the goal')
            return goal

    # Sort candidates and return the best for user_code from ones
    def __choose_best_vertex(self, user_vertex: Vertex, vertices: List[Vertex]) -> Optional[Vertex]:
        'desrciption'

        if len(vertices) == 0:
            return None
        candidates = list(map(lambda vertex: self.get_measured_vertex(user_vertex, vertex), vertices))
        candidates.sort()
        log.info(f'Candidates ids are {([c.vertex.id for c in candidates])}')
        log.info(f'The best vertex id is {candidates[0].vertex.id}')
        return candidates[0].vertex

    # Use '__choose_best_vertex' for choosing the best goal from all ones
    # Note: A goal is a vertex, which has the rate equals 1 and it connects to the end vertex
    def __find_closest_goal(self, user_vertex: Vertex) -> Vertex:
        log.info(f'Goals ids are {[p.id for p in self._graph.end_vertex.parents]}')
        return self.__choose_best_vertex(user_vertex, self._graph.end_vertex.parents)

    # Calculate a set of vertices, which contains all vertices
    # that have a distance (number of diffs) to the goal <= than 'user_code'
    # Run __choose_best_vertex on these vertices, which returns None in case of the empty list
    # Note: we have to remove the 'user_code' from the set
    def __find_closest_vertex_with_path(self, user_vertex: Vertex, goal: Vertex,
                                        to_add_empty: bool = False) -> Optional[Vertex]:
        user_diffs_to_goal = goal.get_dist(user_vertex)
        candidates = []
        vertices = self._graph.get_traversal()
        vertices.remove(self._graph.start_vertex)

        for vertex in vertices:
            # We don't want to add to result the same vertex
            if are_asts_equal(user_vertex.serialized_code.canon_tree, vertex.serialized_code.canon_tree):
                continue
            # Todo: change to normal way (add empy_vertex to graph?)
            if get_code_from_tree(vertex.serialized_code.canon_tree) == '' \
                    and get_code_from_tree(vertex.serialized_code.anon_trees[0]) == '' \
                    and not to_add_empty:
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

    # Choose the best way to go to the goal
    # For example, if we have a good way through the graph, we should advise it,
    # but if don't we would advise going directly to the goal
    def __go_through_graph(self, user_vertex: Vertex, graph_vertex: Vertex, goal: Vertex) -> bool:

        diffs_from_user_to_goal = user_vertex.get_dist(goal)
        diffs_from_empty_to_user = self._empty_vertex.get_dist(user_vertex)
        if PathFinderV1.__is_most_of_path_is_done(diffs_from_empty_to_user + diffs_from_user_to_goal,
                                                  diffs_from_user_to_goal):
            return False

        diffs_from_user_to_graph_vertex = user_vertex.get_dist(graph_vertex)
        return not PathFinderV1.__is_far_from_graph(diffs_from_user_to_goal, diffs_from_user_to_graph_vertex)
