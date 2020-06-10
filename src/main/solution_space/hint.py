# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
import ast
import logging
from typing import Optional, Tuple

from src.main.util import consts
from src.main.canonicalization.consts import TREE_TYPE
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.path_finder.path_finder import IPathFinder
from src.main.solution_space.data_classes import CodeInfo, User, Profile
from src.main.solution_space.consts import HINT_FOLDER, USER_FILE_PREFIX
from src.main.canonicalization.diffs.rivers_diff_handler import RiversDiffHandler
from src.main.solution_space.serialized_code import Code, AnonTree, ISerializedObject
from src.main.canonicalization.canonicalization import get_code_from_tree, get_canon_tree_from_anon_tree, get_imports

log = logging.getLogger(consts.LOGGER_NAME)


class Hint():
    def __init__(self, recommended_code: str):
        self._recommended_code = recommended_code

    @property
    def recommended_code(self) -> str:
        return self._recommended_code


class HintHandler(ISerializedObject):
    def __init__(self, graph: SolutionGraph):
        self._graph = graph
        super().__init__(HINT_FOLDER, USER_FILE_PREFIX)

    @property
    def graph(self) -> str:
        return self._graph

    def create_user_trees(self, source_code: str, profile: Profile,
                          rate: Optional[float] = None) -> Tuple[AnonTree, ast.AST]:
        code_info = CodeInfo(User(profile))
        code = Code.from_source(source_code, rate=rate, task=self._graph.task)
        anon_tree = AnonTree(code.anon_tree, code.rate, self.get_file_path(f'{TREE_TYPE.ANON.value}'), code_info)
        anon_tree.find_medians()
        return anon_tree, code.canon_tree

    @staticmethod
    def get_hint_by_anon_tree(user_source_code: str, next_anon_tree: AnonTree) -> Hint:
        diff_handler = RiversDiffHandler(source_code=user_source_code)
        log.info(f'Next vertex id is {next_anon_tree.id}')

        anon_tree = next_anon_tree.tree
        canon_tree = get_canon_tree_from_anon_tree(anon_tree, get_imports(anon_tree))

        diffs, tree_type = diff_handler.get_diffs(anon_tree, canon_tree)

        log.info(f'The best type of trees is {tree_type.value}')

        # Todo: apply the first diff
        # Todo: new version of apply diffs
        try:
            recommended_tree = diff_handler.apply_diffs(diffs, tree_type)
            return Hint(get_code_from_tree(recommended_tree))
        except UnboundLocalError:
            # Something went wrong in Kelly Rivers applying diffs
            return Hint('UnboundLocalError')

    def get_hint(self, source_code: str, profile: Profile, path_finder: IPathFinder,
                 rate: Optional[float] = None) -> Hint:
        anon_tree, canon_tree = self.create_user_trees(source_code, profile, rate)

        next_anon_tree = path_finder.find_next_anon_tree(anon_tree, canon_tree)
        return HintHandler.get_hint_by_anon_tree(source_code, next_anon_tree)
