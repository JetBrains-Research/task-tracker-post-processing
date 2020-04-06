# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
from src.main.canonicalization.canonicalization import get_code_from_tree
from src.main.canonicalization.diffs.diff_handler import DiffHandler
from src.main.solution_space.data_classes import User
from src.main.solution_space.path_finder import PathFinder
from src.main.solution_space.solution_graph import SolutionGraph


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
        diff_handler = DiffHandler(source_code)
        next_vertex = self._path_finder.find_next_vertex(diff_handler, user)
        diffs_and_types_list = [diff_handler.get_diffs(code_info.anon_tree, next_vertex.code.canon_tree) for code_info in
            next_vertex.code_info_list]
        diffs_len_list = list(map(lambda diffs, type: len(diffs), diffs_and_types_list))
        diffs, type = diffs_and_types_list[diffs_len_list.index(min(diffs_len_list))]
        # Apply the first diff
        recommended_tree = diff_handler.apply_diffs(diffs[:1], type)
        return Hint(get_code_from_tree(recommended_tree))
