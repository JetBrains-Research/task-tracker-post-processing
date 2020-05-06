# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import collections
from itertools import groupby
from typing import List, Optional, Dict, Any

from src.main.solution_space.solution_graph import Vertex
from src.main.solution_space.serialized_code import AnonTree
from src.main.canonicalization.diffs.gumtree import GumTreeDiff
from src.main.solution_space.path_finder.path_finder import IPathFinder, log
from src.main.canonicalization.canonicalization import get_code_from_tree, get_nodes_number_in_ast
from src.main.solution_space.consts import DIFFS_PERCENT_TO_GO_DIRECTLY, DISTANCE_TO_GRAPH_THRESHOLD, CANON_TOP_N,\
    ANON_TOP_N


class PathFinderV3(IPathFinder):

    def find_next_anon_tree(self, user_anon_tree: AnonTree, user_canon_tree: ast.AST) -> AnonTree:
        """
        1. Find the closest goal (__find_closest_goal)
        2. Find the closest graph_vertex (__find_closest_vertex_with_path)
        3. Choose between them using __go_through_graph
        """

        log.info(f'{self.__class__.__name__}\n'
                 f'Start finding the next code state for '
                 f'the user code:\n{get_code_from_tree(user_anon_tree.tree)}\nand '
                 f'the user:\n{user_anon_tree.code_info_list[0].user}')

        goal_anon_tree = self.__find_closest_goal_tree(user_anon_tree)
        log.info(f'Chosen goal anon tree:\n{get_code_from_tree(goal_anon_tree.tree)}')

        graph_anon_tree = self.__find_closest_tree_in_graph(user_anon_tree, user_canon_tree)
        log.info(f'Chosen graph anon tree:\n{get_code_from_tree(graph_anon_tree.tree)}')
        # We can have graph_anon_tree = None
        if graph_anon_tree and self.__go_through_graph(user_anon_tree, graph_anon_tree, goal_anon_tree):
            log.info(f'We are going through graph')
            return graph_anon_tree
        else:
            log.info(f'We are going directly to the goal')
            return goal_anon_tree

    def __choose_best_anon_tree(self, user_anon_tree: AnonTree, anon_trees: List[AnonTree]) -> Optional[AnonTree]:
        """
        1. Sort candidates using MeasuredTree
        2. Return the first candidate
        """
        log.info(f'Number of candidates: {len(anon_trees)}\nCandidates ids are {([a_t.id for a_t in anon_trees])}')
        if len(anon_trees) == 0:
            return None
        candidates = list(map(lambda anon_tree: self.get_measured_tree(user_anon_tree, anon_tree), anon_trees))
        candidates.sort()
        log.info(f'The best vertex id is {candidates[0].candidate_tree.id}')
        return candidates[0].candidate_tree

    # Note: A goal is a vertex, which has the rate equals 1 and it connects to the end vertex
    def __find_closest_goal_tree(self, user_anon_tree: AnonTree) -> AnonTree:
        """
        1. Get list of all goals
        2. Find the closest using __choose_best_vertex()
        """
        goals: List[Vertex] = self._graph.end_vertex.parents
        goals_anon_trees = sum([g.serialized_code.anon_trees for g in goals], [])

        log.info(f'Number of goals: {len(goals)}\nGoals ids are {[g.id for g in goals]}')
        return self.__choose_best_anon_tree(user_anon_tree, goals_anon_trees)

    # Note: we have to remove the 'user_code' from the set
    def __find_closest_tree_in_graph(self, user_anon_tree: AnonTree, user_canon_tree: ast.AST) -> Optional[AnonTree]:
        """
        1. If there is a vertex in the graph with same canon_tree:
            1.1 *find out what to do*
        2. Consider each vertex with similar nodes number as candidate (chose at least TOP_N_CANON candidates)
        """

        # graph_vertex = self._graph.find_vertex(user_canon_tree)
        # # Todo: find a better way
        # if graph_vertex:
        #     graph_anon_tree = graph_vertex.serialized_code.find_anon_tree(user_anon_tree.tree)
        #     if graph_anon_tree:
        #         return self.__find_closest_tree_from_equal_tree(user_anon_tree, graph_anon_tree)

        canon_nodes_number = get_nodes_number_in_ast(user_canon_tree)
        anon_nodes_number = user_anon_tree.nodes_number

        # Get vertices ids with canon trees, which have nodes number similar to user canon_nodes_number
        vertices_ids = self.__get_top_n_candidates(CANON_TOP_N, canon_nodes_number, self._graph.canon_trees_nodes_number)
        vertices: List[Vertex] = [Vertex.get_item_by_id(id) for id in vertices_ids]

        anon_trees = sum([v.serialized_code.anon_trees for v in vertices], [])
        anon_nodes_numbers_dict = {k: list(v) for k, v in groupby(anon_trees, lambda a_t: a_t.nodes_number)}
        anon_candidates = self.__get_top_n_candidates(ANON_TOP_N, anon_nodes_number, anon_nodes_numbers_dict)

        return self.__choose_best_anon_tree(user_anon_tree, anon_candidates)

    def __find_closest_tree_from_equal_tree(self, user_anon_tree: AnonTree, equal_anon_tree: AnonTree) -> AnonTree:
        log.info('Found the same anon tree')
        # Todo: what to do if there is the exact vertex? Find a path to the goal? Now just returning it
        return equal_anon_tree

    # Todo: speed it up due to sparse node_numbers dict
    @staticmethod
    def __get_top_n_candidates(top_n: int, nodes_number: int, nodes_numbers_dict: Dict[int, List[Any]]) -> List[Any]:
        """
        We want to have top_n trees with nodes number, that is close to the given nodes_number.
        So we consequently add vertices with node numbers equal:
        1. nodes_number
        2. nodes_number - 1, nodes_number + 1
        3. nodes_number - 2, nodes_number + 2
        4. ....
        until we reach top_n or have no more node_numbers to add
        """
        candidates = []
        nodes_numbers_queue = collections.deque([nodes_number])

        lower_bound = nodes_number
        upper_bound = nodes_number
        max_nodes_number = max(nodes_numbers_dict.keys())
        min_nodes_number = min(nodes_numbers_dict.keys())

        while len(candidates) < top_n and nodes_numbers_queue:
            while nodes_numbers_queue:
                nodes_number = nodes_numbers_queue.pop()
                candidates += nodes_numbers_dict.get(nodes_number, [])

            lower_bound -= 1
            if lower_bound >= min_nodes_number:
                nodes_numbers_queue.append(lower_bound)
            upper_bound += 1

            if lower_bound <= max_nodes_number:
                nodes_numbers_queue.append(upper_bound)

        return candidates

    @staticmethod
    def __is_far_from_graph(diffs_from_user_to_goal: int, diffs_from_user_to_graph_vertex: int) -> bool:
        return diffs_from_user_to_graph_vertex / diffs_from_user_to_goal > DISTANCE_TO_GRAPH_THRESHOLD

    @staticmethod
    def __is_most_of_path_is_done(diffs_from_empty_to_goal: int, diffs_from_user_to_goal: int) -> bool:
        return diffs_from_user_to_goal <= diffs_from_empty_to_goal * DIFFS_PERCENT_TO_GO_DIRECTLY

    @staticmethod
    def __is_rate_worse(user_rate: float, graph_vertex_rate: float) -> bool:
        # TODO: 14/04 or If number of passed tests > 0 then True???
        return user_rate > 0 and graph_vertex_rate == 0

    # Returns should we go through graph or directly to the goal
    def __go_through_graph(self, user_anon: AnonTree, graph_anon: AnonTree, goal_anon: AnonTree) -> bool:
        """
        1. If __is_most_of_path_is_done, return False
        2. If __is_rate_worse, return False
        3. Return not __is_far_from_graph
        """
        empty_anon = self._graph.empty_vertex.serialized_code.anon_trees[0]
        diffs_from_user_to_goal = GumTreeDiff.get_diffs_number(user_anon.tree_file, goal_anon.tree_file)
        diffs_from_empty_to_user = GumTreeDiff.get_diffs_number(empty_anon.tree_file, user_anon.tree_file)
        if self.__is_most_of_path_is_done(diffs_from_empty_to_user + diffs_from_user_to_goal,
                                          diffs_from_user_to_goal):
            log.info('Most of path is done')
            return False

        # Todo: add is_rate_worse

        diffs_from_user_to_graph_vertex = GumTreeDiff.get_diffs_number(user_anon.tree_file, graph_anon.tree_file)
        return not self.__is_far_from_graph(diffs_from_user_to_goal, diffs_from_user_to_graph_vertex)
