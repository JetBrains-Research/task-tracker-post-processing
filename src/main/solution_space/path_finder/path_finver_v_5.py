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
from src.main.canonicalization.canonicalization import get_code_from_tree, get_nodes_number_in_ast


class PathFinderV5(IPathFinder):
    candidates_file_prefix: Optional[str] = None

    canon_top_n = 15
    anon_top_n = 5
    same_structure_top_n = 7

    max_tree_nodes_number_indent = 5
    max_goal_nodes_number_indent = 15

    nodes_number_percent_close_to_goals = 0.2
    diffs_percent_path_is_done = 0.2
    diffs_percent_far_from_graph = 0.2

    graph_tree_stop_earlier = False
    graph_tree_lower_bound = True

    goal_tree_stop_earlier = False
    goal_tree_lower_bound = True

    to_add_empty_tree_to_goals = False
    to_add_empty_tree_to_graph = True

    to_add_same_structure_trees_to_goals = False
    to_add_same_structure_trees_to_graph = True

    @doc_param(graph_tree_stop_earlier, graph_tree_lower_bound, goal_tree_stop_earlier, goal_tree_lower_bound,
               to_add_empty_tree_to_graph, to_add_empty_tree_to_goals)
    def find_next_anon_tree(self, user_anon_tree: AnonTree, user_canon_tree: ast.AST,
                            candidates_file_id: Optional[str] = None) -> AnonTree:
        """
        1. Find the same tree SAME_TREE in the graph and get the best tree from next trees (__find_same_tree_in_graph)
        2. If SAME_TREE is not None, return SAME_TREE
        2. Find the closest tree CLOSEST_TREE in graph (__find_closest_tree with graph.canon_trees_nodes_number,
        can_stop_earlier={0}, to_use_lower_bound={1}, to_add_empty_tree_to_graph={4})
        3. If not _is_close_to_goals, return CLOSEST_TREE
        4. Find the closest goal CLOSEST_GOAL in graph (__find_closest_goal_tree, can_stop_earlier={2},
         to_use_lower_bound={3}, to_add_empty_tree_to_goals={5})
        5. Choose between CLOSEST_TREE and CLOSEST_GOAL using __go_through_graph
        """

        log.info(f'{self.__class__.__name__}\n'
                 f'Start finding the next code state for '
                 f'the user code:\n{get_code_from_tree(user_anon_tree.tree)}\nand '
                 f'the user:\n{user_anon_tree.code_info_list[0].user}')

        self.candidates_file_prefix = f'{self.get_file_prefix_by_user_tree(candidates_file_id)}'
        same_tree = self.__find_same_tree_in_graph(user_anon_tree, user_canon_tree)
        if same_tree is not None:
            log.info(f'Found the same tree. Chosen anon tree:\n{get_code_from_tree(same_tree.tree)}')
            print('same tree')
            return same_tree

        log.info('Same tree not found')

        canon_nodes_number = get_nodes_number_in_ast(user_canon_tree)
        graph_anon_tree = self.__find_closest_tree(user_anon_tree, canon_nodes_number,
                                                   self.graph.canon_nodes_number_dict,
                                                   to_use_lower_bound=self.graph_tree_lower_bound,
                                                   can_stop_earlier=self.graph_tree_stop_earlier,
                                                   candidates_file_name='graph_candidates',
                                                   to_add_empty_tree=self.to_add_empty_tree_to_graph,
                                                   to_add_same_structure_trees=self.to_add_same_structure_trees_to_graph)
        # We can have graph_anon_tree = None
        if graph_anon_tree:
            log.info(f'Chosen anon tree in graph:\n{get_code_from_tree(graph_anon_tree.tree)}')
            if not self.__is_close_to_goals(graph_anon_tree):
                log.info(f'The most of path is not done. Go through graph')
                print('graph tree')
                return graph_anon_tree

        goal_anon_tree = self.__find_closest_goal_tree(user_anon_tree, canon_nodes_number)
        log.info(f'Chosen goal anon tree:\n{get_code_from_tree(goal_anon_tree.tree)}')

        # We can have graph_anon_tree = None
        if graph_anon_tree and self.__go_through_graph(user_anon_tree, graph_anon_tree, goal_anon_tree):
            log.info(f'We are going through graph')
            print('goal tree')
            return graph_anon_tree
        else:
            log.info(f'We are going directly to the goal')
            print('goal tree')
            return goal_anon_tree

    def __find_same_tree_in_graph(self, user_anon_tree: AnonTree, user_canon_tree: ast.AST) -> Optional[AnonTree]:
        """
        1. Find the user anon tree ANON_TREE in the graph
        2. Filter all ANON_TREE.next_anon_trees, taking trees with nodes number >= user nodes number
        3. Sort next_anon_trees, using MeasuredTree
        4. Return the first candidate
        """
        graph_vertex = self._graph.find_vertex(user_canon_tree)
        if graph_vertex:
            graph_anon_tree = graph_vertex.serialized_code.find_anon_tree(user_anon_tree.tree)
            if graph_anon_tree:
                next_anon_trees = [AnonTree.get_item_by_id(id) for id in graph_anon_tree.next_anon_trees_ids]
                next_anon_trees = [tree for tree in next_anon_trees if tree.nodes_number >= user_anon_tree.nodes_number]
                return self.__choose_best_anon_tree(user_anon_tree, next_anon_trees, 'same_tree_candidates')
        return None

    @staticmethod
    def __get_items_nodes_number_dict(items: List[Any]) -> Dict[int, list]:
        return {k: list(v) for k, v in groupby(items, lambda item: item.nodes_number)}

    @doc_param(anon_top_n, canon_top_n, same_structure_top_n)
    def __find_closest_tree(self, user_anon_tree: AnonTree, user_canon_nodes_number: int,
                            canon_nodes_numbers_dict: Dict[int, list],
                            candidates_file_name: str,
                            can_stop_earlier: bool = True,
                            to_use_lower_bound: bool = True,
                            to_add_empty_tree: bool = False,
                            to_add_same_structure_trees: bool = False) -> Optional[AnonTree]:
        """
        1. Consider each vertex with similar nodes number as candidate (chose at least TOP_N_CANON = {1} candidates)
        2. Choose at least TOP_N_ANON = {0} anon trees from canon candidates
        3. Consider each anon tree with same structure as candidate
        4. Choose at least {2} trees according to nodes number from same tree candidates
        4. Add empty tree if needed
        5. Run __choose_best_anon_tree on all candidates
        """

        # Get vertices ids with canon trees, which have nodes number similar to user canon_nodes_number
        vertices_ids = self.__get_top_n_candidates(self.canon_top_n, user_canon_nodes_number, canon_nodes_numbers_dict,
                                                   can_stop_earlier, to_use_lower_bound)
        log.info(f'CANON_TOP_N vertices ids are {vertices_ids}')
        anon_candidates = []

        if len(vertices_ids) != 0:
            vertices: List[Vertex] = [Vertex.get_item_by_id(id) for id in vertices_ids]
            anon_trees = sum([v.serialized_code.anon_trees for v in vertices], [])
            anon_nodes_numbers_dict = self.__get_items_nodes_number_dict(anon_trees)
            anon_candidates = self.__get_top_n_candidates(self.anon_top_n, user_anon_tree.nodes_number,
                                                          anon_nodes_numbers_dict,
                                                          can_stop_earlier, to_use_lower_bound)
        if to_add_empty_tree:
            anon_candidates.append(self._graph.empty_vertex.serialized_code.anon_trees[0])

        if to_add_same_structure_trees:
            anon_candidates += self.__get_same_structure_trees(user_anon_tree, self.same_structure_top_n)

        return self.__choose_best_anon_tree(user_anon_tree, anon_candidates, candidates_file_name)

    def __get_same_structure_trees(self, user_anon_tree: AnonTree, trees_number: int) -> List[AnonTree]:
        same_structure_anon_trees = [AnonTree.get_item_by_id(a_id) for a_id in
                                     self.graph.anon_structure_dict[user_anon_tree.ast_structure]]
        same_structure_anon_trees_dict = self.__get_items_nodes_number_dict(same_structure_anon_trees)
        same_structure_candidates = self.__get_top_n_candidates(trees_number, user_anon_tree.nodes_number,
                                                                same_structure_anon_trees_dict,
                                                                can_stop_earlier=False, to_use_lower_bound=True)
        log.info(f'Found trees with same structure: {[c.id for c in same_structure_candidates]}')
        return same_structure_candidates

    @doc_param(nodes_number_percent_close_to_goals, max_goal_nodes_number_indent)
    def __is_close_to_goals(self, closest_tree: AnonTree) -> bool:
        """
        1. Use only nodes number info.
        2. Returns True if percent of goals with similar nodes number (with indent no more than {1}) is more than {0}
        """
        if self.graph.is_goals_median_empty():
            log.info('Cannot check if close to goals because goals median is empty')
            return False
        # Todo: make it better
        goals_nodes_number = sum([[k] * len(v) for k, v in self.graph.goals_nodes_number_dict.items()], [])
        count_similar_trees = 0
        for g_n in goals_nodes_number:
            if abs(g_n - closest_tree.nodes_number) <= self.max_goal_nodes_number_indent:
                count_similar_trees += 1
        return count_similar_trees / len(goals_nodes_number) >= 1 - self.nodes_number_percent_close_to_goals

    @doc_param(canon_top_n)
    def __find_closest_goal_tree(self, user_anon_tree: AnonTree, user_canon_nodes_number: int) -> AnonTree:
        """
        1. Get list of all goals
        2. Chose at least TOP_N_CANON = {0} candidates, using lower bound and nod stopping earlier
        2. Find the closest using __choose_best_vertex()
        """
        return self.__find_closest_tree(user_anon_tree, user_canon_nodes_number, self.graph.goals_nodes_number_dict,
                                        candidates_file_name='goal_candidates',
                                        can_stop_earlier=self.goal_tree_stop_earlier,
                                        to_use_lower_bound=self.goal_tree_lower_bound,
                                        to_add_empty_tree=self.to_add_empty_tree_to_goals,
                                        to_add_same_structure_trees=self.to_add_same_structure_trees_to_goals)

    # Todo: speed it up due to sparse node_numbers dict
    @staticmethod
    @doc_param(max_tree_nodes_number_indent)
    def __get_top_n_candidates(top_n: int, nodes_number: int, nodes_numbers_dict: Dict[int, List[Any]],
                               can_stop_earlier: bool = True, to_use_lower_bound: bool = False) -> List[Any]:
        """
        We want to have top_n trees with nodes number, that is close to the given nodes_number.
        So we consequently add vertices with node numbers equal:
        1. nodes_number
        2. nodes_number - 1 (if lower bound is on), nodes_number + 1
        3. nodes_number - 2 (if lower bound is on), nodes_number + 2
        4. ....
        until we reach top_n or have no more node_numbers to add.
        If can_stop_earlier is True, we stop as soon as we far  from user nodes number at {0} nodes numbers
        """
        log.info(f'Start getting top_n candidates, top_n is {top_n}, nodes number is {nodes_number}')
        candidates = []
        nodes_numbers_queue = collections.deque([nodes_number])
        indent = 0
        if not nodes_numbers_dict:
            log.info(f'Given nodes_number_dict is empty, finish getting top_n candidates, top_n is {top_n},'
                     f' candidates len is {len(candidates)}')
            return candidates
        max_nodes_number = max(nodes_numbers_dict.keys())
        min_nodes_number = min(nodes_numbers_dict.keys())

        while len(candidates) < top_n and nodes_numbers_queue and \
                (not can_stop_earlier or indent <= PathFinderV5.max_tree_nodes_number_indent):
            log.info(f'Start adding candidates.\n'
                     f'Candidates len is {len(candidates)}, queue have {len(nodes_numbers_queue)} nodes numbers')
            while nodes_numbers_queue:
                new_nodes_number = nodes_numbers_queue.pop()
                candidates += nodes_numbers_dict.get(new_nodes_number, [])

            log.info(f'Finish adding candidates.\n'
                     f'Candidates len is {len(candidates)}, queue have {len(nodes_numbers_queue)} nodes numbers')

            indent += 1

            if to_use_lower_bound:
                lower_bound = nodes_number - indent
                if lower_bound >= min_nodes_number:
                    log.info(f'Append lower_bound to queue: {lower_bound}, min nodes number is {min_nodes_number}')
                    nodes_numbers_queue.append(lower_bound)

            upper_bound = nodes_number + indent
            if upper_bound <= max_nodes_number:
                log.info(f'Append upper_bound to queue: {upper_bound}, max nodes number is {max_nodes_number}')
                nodes_numbers_queue.append(upper_bound)

        log.info(f'Finish getting top_n candidates, top_n is {top_n}, candidates len is {len(candidates)}')
        return candidates

    def __choose_best_anon_tree(self, user_anon_tree: AnonTree, anon_trees: List[AnonTree],
                                candidates_file_name: str) -> Optional[AnonTree]:
        """
        1. Sort candidates using MeasuredTree
        2. Return the first candidate
        """
        log.info(f'Number of candidates: {len(anon_trees)}\nCandidates ids are {([a_t.id for a_t in anon_trees])}')
        anon_trees = list(set(anon_trees))
        log.info(f'Number of candidates: {len(anon_trees)}\nCandidates ids are {([a_t.id for a_t in anon_trees])}')

        if len(anon_trees) == 0:
            return None
        candidates = list(map(lambda anon_tree: self.get_measured_tree(user_anon_tree, anon_tree), anon_trees))

        self.write_candidates_info_to_file(candidates, f'{self.candidates_file_prefix}_{candidates_file_name}')

        candidates.sort()
        log.info(f'The best vertex id is {candidates[0].candidate_tree.id}')
        return candidates[0].candidate_tree

    @staticmethod
    @doc_param(diffs_percent_far_from_graph)
    def __is_far_from_graph(diffs_from_user_to_goal: int, diffs_from_user_to_graph_vertex: int) -> bool:
        """
        Returns True, if diffs from USER to GRAPH_VERTEX is more than {0} * (diffs from USER to GOAL)
        """
        return diffs_from_user_to_graph_vertex > PathFinderV5.diffs_percent_far_from_graph * diffs_from_user_to_goal

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
        return diffs_from_user_to_goal <= PathFinderV5.diffs_percent_path_is_done * diffs_from_empty_to_goal

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
