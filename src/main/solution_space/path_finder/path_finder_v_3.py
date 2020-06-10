# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import collections
from itertools import groupby
from typing import List, Optional, Dict, Any

from src.main.solution_space.solution_graph import Vertex
from src.main.solution_space.serialized_code import AnonTree
from src.main.canonicalization.diffs.gumtree import GumTreeDiff
from src.main.solution_space.path_finder_test_system import doc_param, skip
from src.main.solution_space.path_finder.path_finder import IPathFinder, log
from src.main.canonicalization.canonicalization import get_code_from_tree, AstStructure


@skip(reason='The best version is PathFinderV4')
class PathFinderV3(IPathFinder):
    candidates_file_prefix: Optional[str] = None
    canon_top_n = 5
    anon_top_n = 10
    nodes_number_percent_close_to_goals = 0.2
    diffs_percent_path_is_done = 0.2
    diffs_percent_far_from_graph = 0.2

    def find_next_anon_tree(self, user_anon_tree: AnonTree, user_canon_tree: ast.AST,
                            candidates_file_id: Optional[int] = None) -> AnonTree:
        """
        1. Find the same tree SAME_TREE in the graph and get the best tree from next trees (__find_same_tree_in_graph)
        2. If SAME_TREE is not None, return SAME_TREE
        2. Find the closest tree CLOSEST_TREE in graph (__find_closest_tree with graph.canon_trees_nodes_number)
        3. If not _is_close_to_goals, return CLOSEST_TREE
        4. Find the closest goal CLOSEST_GOAL in graph (__find_closest_goal_tree)
        5. Choose between CLOSEST_TREE and CLOSEST_GOAL using __go_through_graph
        """

        log.info(f'{self.__class__.__name__}\n'
                 f'Start finding the next code state for '
                 f'the user code:\n{get_code_from_tree(user_anon_tree.tree)}\nand '
                 f'the user:\n{user_anon_tree.code_info_list[0].user}')

        self.candidates_file_prefix = f'{self.get_file_prefix_by_user_tree(user_anon_tree, candidates_file_id)}'
        same_tree = self.__find_same_tree_in_graph(user_anon_tree, user_canon_tree)
        if same_tree is not None:
            log.info(f'Found the same tree. Chosen anon tree:\n{get_code_from_tree(same_tree.tree)}')
            return same_tree

        log.info('Same tree not found')

        canon_nodes_number = AstStructure.get_nodes_number_in_ast(user_canon_tree)
        graph_anon_tree = self.__find_closest_tree(user_anon_tree, canon_nodes_number,
                                                   self.graph.canon_nodes_number_dict,
                                                   candidates_file_name='graph_candidates')
        log.info(f'Chosen anon tree in graph:\n{get_code_from_tree(graph_anon_tree.tree)}')
        if not self._is_close_to_goals(graph_anon_tree):
            log.info(f'The most of path is not done. Go through graph')
            return graph_anon_tree

        goal_anon_tree = self.__find_closest_goal_tree(user_anon_tree, canon_nodes_number)
        log.info(f'Chosen goal anon tree:\n{get_code_from_tree(goal_anon_tree.tree)}')

        # We can have graph_anon_tree = None
        if graph_anon_tree and self.__go_through_graph(user_anon_tree, graph_anon_tree, goal_anon_tree):
            log.info(f'We are going through graph')
            return graph_anon_tree
        else:
            log.info(f'We are going directly to the goal')
            return goal_anon_tree

    def __find_same_tree_in_graph(self, user_anon_tree: AnonTree, user_canon_tree: ast.AST) -> Optional[AnonTree]:
        """
        1. Find the user anon tree ANON_TREE in the graph
        2. Sort ANON_TREE.next_anon_trees using MeasuredTree
        3. Return the first candidate
        """
        graph_vertex = self._graph.find_vertex(user_canon_tree)
        if graph_vertex:
            graph_anon_tree = graph_vertex.serialized_code.find_anon_tree(user_anon_tree.tree)
            if graph_anon_tree:
                next_anon_trees = [AnonTree.get_item_by_id(id) for id in graph_anon_tree.next_anon_trees_ids]
                self.write_candidates_info_to_file(next_anon_trees,
                                                   f'{self.candidates_file_prefix}_same_tree_candidates')
                return self.__choose_best_anon_tree(user_anon_tree, next_anon_trees)
        return None

    @staticmethod
    def __get_items_nodes_number_dict(items: List[Any]) -> Dict[int, list]:
        return {k: list(v) for k, v in groupby(items, lambda item: item.nodes_number)}

    @doc_param(anon_top_n, canon_top_n)
    def __find_closest_tree(self, user_anon_tree: AnonTree, user_canon_nodes_number: int,
                            canon_nodes_numbers_dict: Dict[int, list],
                            candidates_file_name: str) -> Optional[AnonTree]:
        """
        1. Consider each vertex with similar nodes number as candidate (chose at least TOP_N_CANON = {1} candidates)
        2. Choose at least TOP_N_ANON = {0} anon trees from canon candidates and run __choose_best_anon_tree
        """

        # Get vertices ids with canon trees, which have nodes number similar to user canon_nodes_number
        vertices_ids = self.__get_top_n_candidates(self.canon_top_n, user_canon_nodes_number, canon_nodes_numbers_dict)
        log.info(f'CANON_TOP_N vertices ids are {vertices_ids}')
        vertices: List[Vertex] = [Vertex.get_item_by_id(id) for id in vertices_ids]

        anon_trees = sum([v.serialized_code.anon_trees for v in vertices], [])
        anon_nodes_numbers_dict = self.__get_items_nodes_number_dict(anon_trees)
        anon_candidates = self.__get_top_n_candidates(self.anon_top_n, user_anon_tree.nodes_number, anon_nodes_numbers_dict)

        self.write_candidates_info_to_file(anon_candidates, f'{self.candidates_file_prefix}_{candidates_file_name}')
        return self.__choose_best_anon_tree(user_anon_tree, anon_candidates)

    @doc_param(nodes_number_percent_close_to_goals)
    def _is_close_to_goals(self, closest_tree: AnonTree) -> bool:
        """
        1. Use only nodes number info.
        2. Returns True, if closest_tree nodes number is more, than {0} * median for goals nodes number
        """
        # if self.graph.median_goals_nodes_numbers
        if self.graph.is_goals_median_empty():
            log.info('Cannot check if close to goals because goals median is empty')
            return False

        # Todo: don't we want to use 0.8 here instead of 0.2??
        return closest_tree.nodes_number >= self.graph.goals_median * self.nodes_number_percent_close_to_goals

    @doc_param(canon_top_n)
    def __find_closest_goal_tree(self, user_anon_tree: AnonTree, user_canon_nodes_number: int) -> AnonTree:
        """
        1. Get list of all goals
        2. Chose at least TOP_N_CANON = {0} candidates
        2. Find the closest using __choose_best_vertex()
        """
        return self.__find_closest_tree(user_anon_tree, user_canon_nodes_number, self.graph.goals_nodes_number_dict,
                                        candidates_file_name='goal_candidates')

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
        log.info(f'Start getting top_n candidates, top_n is {top_n}, nodes number is {nodes_number}')
        candidates = []
        nodes_numbers_queue = collections.deque([nodes_number])

        lower_bound = nodes_number
        upper_bound = nodes_number
        max_nodes_number = max(nodes_numbers_dict.keys())
        min_nodes_number = min(nodes_numbers_dict.keys())

        while len(candidates) < top_n and nodes_numbers_queue:
            log.info(f'Start adding candidates.\n'
                     f'Candidates len is {len(candidates)}, queue have {len(nodes_numbers_queue)} nodes numbers')
            while nodes_numbers_queue:
                nodes_number = nodes_numbers_queue.pop()
                candidates += nodes_numbers_dict.get(nodes_number, [])

            log.info(f'Finish adding candidates.\n'
                     f'Candidates len is {len(candidates)}, queue have {len(nodes_numbers_queue)} nodes numbers')

            lower_bound -= 1
            if lower_bound >= min_nodes_number:
                log.info(f'Append lower_bound to queue: {lower_bound}, min nodes number is {min_nodes_number}')
                nodes_numbers_queue.append(lower_bound)

            upper_bound += 1
            if upper_bound <= max_nodes_number:
                log.info(f'Append upper_bound to queue: {upper_bound}, max nodes number is {max_nodes_number}')
                nodes_numbers_queue.append(upper_bound)

        log.info(f'Finish getting top_n candidates, top_n is {top_n}, candidates len is {len(candidates)}')
        return candidates

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

    @staticmethod
    @doc_param(diffs_percent_far_from_graph)
    def __is_far_from_graph(diffs_from_user_to_goal: int, diffs_from_user_to_graph_vertex: int) -> bool:
        """
        Returns True, if diffs from USER to GRAPH_VERTEX is more than {0} * (diffs from USER to GOAL)
        """
        return diffs_from_user_to_graph_vertex > PathFinderV3.diffs_percent_far_from_graph * diffs_from_user_to_goal

    @staticmethod
    def __is_rate_worse(user_rate: float, graph_vertex_rate: float) -> bool:
        # TODO: 14/04 or If number of passed tests > 0 then True???
        return user_rate > 0 and graph_vertex_rate == 0

    @staticmethod
    @doc_param(diffs_percent_path_is_done)
    def __is_most_of_path_is_done(diffs_from_empty_to_goal: int, diffs_from_user_to_goal: int) -> bool:
        """
        Returns True, if diff from USER to GOAL is less than {0} * (diffs from EMPTY to GOAL)
        """
        return diffs_from_user_to_goal <= PathFinderV3.diffs_percent_path_is_done * diffs_from_empty_to_goal

    # Returns should we go through graph or directly to the goal
    def __go_through_graph(self, user_anon: AnonTree, graph_anon: AnonTree, goal_anon: AnonTree) -> bool:
        """
        1. If __is_rate_worse, return False
        2. If __is_most_of_path_is_done, return False
        2. Return not __is_far_from_graph
        """
        empty_anon = self._graph.empty_vertex.serialized_code.anon_trees[0]
        diffs_from_empty_to_user = GumTreeDiff.get_diffs_number(empty_anon.tree_file, user_anon.tree_file)
        diffs_from_user_to_goal = GumTreeDiff.get_diffs_number(user_anon.tree_file, goal_anon.tree_file)

        if self.__is_most_of_path_is_done(diffs_from_empty_to_user + diffs_from_user_to_goal,
                                          diffs_from_user_to_goal):
            log.info('Most of path is done')
            return False

        # Todo: add is_rate_worse

        diffs_from_user_to_graph_vertex = GumTreeDiff.get_diffs_number(user_anon.tree_file, graph_anon.tree_file)
        return not self.__is_far_from_graph(diffs_from_user_to_goal, diffs_from_user_to_graph_vertex)
