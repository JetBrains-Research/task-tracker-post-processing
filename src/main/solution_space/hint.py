# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
import logging

from src.main.util import consts
from src.main.solution_space.data_classes import User
from src.main.solution_space.path_finder.path_finder import PathFinder
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.canonicalization.diffs.rivers_diff_handler import RiversDiffHandler
from src.main.canonicalization.canonicalization import get_code_from_tree


log = logging.getLogger(consts.LOGGER_NAME)


class Hint:
    def __init__(self, recommended_code: str):
        self._recommended_code = recommended_code

    @property
    def recommended_code(self) -> str:
        return self._recommended_code


# Todo: find a better name
class HintGetter:
    def __init__(self, graph: SolutionGraph):
        self._graph = graph
        self._path_finder = PathFinder(graph)

    @property
    def graph(self) -> str:
        return self._graph

    def get_hint(self, source_code: str, user: User) -> Hint:
        diff_handler = RiversDiffHandler(source_code=source_code)
        next_vertex = self._path_finder.find_next_vertex(diff_handler, user)
        log.info(f'Next vertex id is {next_vertex.id}')
        diffs_and_types_list = [diff_handler.get_diffs(a_t, next_vertex.code.canon_tree)
                                for a_t in next_vertex.code.anon_trees]
        diffs_len_list = list(map(lambda diff_and_type: len(diff_and_type[0]), diffs_and_types_list))
        diffs, type = diffs_and_types_list[diffs_len_list.index(min(diffs_len_list))]
        log.info(f'The best type of trees is {type.value}')
        # Apply the first diff
        # Todo: new vwrsion of apply diffs
        recommended_tree = diff_handler.apply_diffs(diffs, type)
        return Hint(get_code_from_tree(recommended_tree))
