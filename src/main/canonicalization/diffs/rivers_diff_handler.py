# Copyright (c) 2017 Kelly Rivers
# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging
from typing import List, Tuple, Optional

from src.main.util import consts
from src.main.canonicalization.consts import TREE_TYPE
from src.main.util.log_util import log_and_raise_error
from src.main.canonicalization.diffs.individualize import mapEdit
from src.main.canonicalization.diffs.diff_handler import IDiffHandler
from src.main.canonicalization.canonicalization import get_code_from_tree
from src.main.canonicalization.diffs.generate_next_states import updateChangeVectors
from src.main.canonicalization.diffs.diff_asts import diffAsts, printFunction, ChangeVector, deepcopy

log = logging.getLogger(consts.LOGGER_NAME)


class RiversDiffHandler(IDiffHandler):

    def get_diffs(self, anon_dst_tree: ast.AST, canon_dst_tree: ast.AST) -> Tuple[List[ChangeVector], TREE_TYPE]:
        anon_diffs = diffAsts(self._anon_tree, anon_dst_tree)
        canon_diffs = diffAsts(self._canon_tree, canon_dst_tree)
        log.info(f'Number of diffs between anonymized trees is {len(anon_diffs)}\n'
                 f'Number of diffs between canonicalized trees is {len(canon_diffs)}')

        if len(anon_diffs) <= len(canon_diffs):
            log.info(f'Anonymized trees were selected')
            anon_diffs, _ = updateChangeVectors(anon_diffs, self._anon_tree, self._anon_tree)
            return anon_diffs, TREE_TYPE.ANON
        log.info(f'Canonicalized trees were selected')
        canon_diffs, _ = updateChangeVectors(canon_diffs, self._canon_tree, self._canon_tree)
        return canon_diffs, TREE_TYPE.CANON

    def get_diffs_from_diff_handler(self, diff_handler: IDiffHandler) -> Tuple[List[ChangeVector], TREE_TYPE]:
        return self.get_diffs(diff_handler.anon_tree, diff_handler._canon_tree)

    def get_diffs_number(self, anon_dst_tree: Optional[ast.AST], canon_dst_tree: Optional[ast.AST]) -> int:
        if anon_dst_tree is None or canon_dst_tree is None:
            log_and_raise_error(f'Trees can not be empty!\nAnon tree:\n{get_code_from_tree(anon_dst_tree)}\n'
                                f'Canon tree:\n{get_code_from_tree(canon_dst_tree)}', log)
        return len(self.get_diffs(anon_dst_tree, canon_dst_tree)[0])

    def apply_diffs(self, diffs: List[ChangeVector], tree_type: TREE_TYPE = TREE_TYPE.CANON) -> ast.AST:
        source_tree = deepcopy(self._orig_tree)
        if len(diffs) == 0:
            return source_tree

        current_source_tree = None
        if tree_type == TREE_TYPE.ANON:
            current_source_tree = self._anon_tree
        elif tree_type == TREE_TYPE.CANON:
            current_source_tree = self._canon_tree
        else:
            log_and_raise_error(f'Unsupported tree type {tree_type}', log)

        diffs = mapEdit(current_source_tree, source_tree, diffs)
        for e in diffs:
            e.start = source_tree
            source_tree = e.applyChange()
        log.info(f'Source code before applying diffs is:\n{printFunction(self._orig_tree)}\n'
                 f'Source code after applying diffs is:\n{printFunction(source_tree)}')
        return source_tree
