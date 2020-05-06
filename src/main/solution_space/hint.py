# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

from src.main.util import consts
from src.main.solution_space.data_classes import CodeInfo
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.path_finder.path_finder import IPathFinder
from src.main.solution_space.measured_vertex.measured_tree import IMeasuredTree
from src.main.canonicalization.diffs.rivers_diff_handler import RiversDiffHandler
from src.main.solution_space.serialized_code import Code, AnonTree, SerializedCode
from src.main.canonicalization.canonicalization import get_code_from_tree, Type, get_canon_tree_from_anon_tree, \
    get_imports

log = logging.getLogger(consts.LOGGER_NAME)


class Hint:
    def __init__(self, recommended_code: str):
        self._recommended_code = recommended_code

    @property
    def recommended_code(self) -> str:
        return self._recommended_code


class HintHandler:
    def __init__(self, graph: SolutionGraph, path_finder: Type[IPathFinder], measured_vertex: Type[IMeasuredTree]):
        self._graph = graph
        self._path_finder = path_finder(graph, measured_vertex)

    @property
    def graph(self) -> str:
        return self._graph

    @property
    def path_finder(self) -> IPathFinder:
        return self._path_finder

    def get_hint(self, source_code: str, code_info: CodeInfo) -> Hint:
        code = Code.from_source(source_code, rate=None, task=self._graph.task)
        serialized_code = SerializedCode(code, code_info, self._graph.graph_directory, self._graph.file_prefix)
        anon_tree = serialized_code.anon_trees[0]

        next_anon_tree = self.path_finder.find_next_anon_tree(anon_tree, code.canon_tree)
        diff_handler = RiversDiffHandler(source_code=source_code)
        log.info(f'Next vertex id is {next_anon_tree.id}')

        anon_tree = next_anon_tree.tree
        canon_tree = get_canon_tree_from_anon_tree(anon_tree, get_imports(anon_tree))

        diffs, tree_type = diff_handler.get_diffs(anon_tree, canon_tree)

        log.info(f'The best type of trees is {tree_type.value}')

        # Todo: apply the first diff
        # Todo: new version of apply diffs
        recommended_tree = diff_handler.apply_diffs(diffs, tree_type)
        return Hint(get_code_from_tree(recommended_tree))
