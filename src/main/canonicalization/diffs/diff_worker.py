# Copyright (c) 2017 Kelly Rivers
# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging

from typing import List, Tuple
from src.main.util import consts
from src.main.canonicalization.consts import TREE_TYPE
from src.main.canonicalization.diffs.individualize import mapEdit
from src.main.canonicalization.diffs.diff_asts import diffAsts, printFunction, ChangeVector, deepcopy
from src.main.canonicalization.canonicalization import get_canonicalized_and_orig_form, get_canonicalized_form


log = logging.getLogger(consts.LOGGER_NAME)


class DiffWorker:
    def __init__(self, source_code: str):
        self._anon_source_tree, self._orig_source_tree = get_canonicalized_and_orig_form(source_code, only_anon=True)
        self._canon_source_tree = get_canonicalized_form(self._anon_source_tree)

    @property
    def orig_source_tree(self) -> ast.AST:
        return self._orig_source_tree

    @property
    def anon_source_tree(self) -> ast.AST:
        return self._anon_source_tree

    @property
    def canon_source_tree(self) -> ast.AST:
        return self._canon_source_tree

    def get_diffs(self, anon_dst_tree: ast.AST, canon_dst_tree: ast.AST) -> Tuple[List[ChangeVector], TREE_TYPE]:
        anon_edits = diffAsts(self._anon_source_tree, anon_dst_tree)
        canon_edits = diffAsts(self._canon_source_tree, canon_dst_tree)
        log.info(f'Number of edits between anonymized trees is {anon_edits}\n'
                 f'Number of edits between canonicalized trees is {canon_edits}')

        if len(anon_edits) <= len(canon_edits):
            log.info(f'Anonymized trees was selected')
            return anon_edits, TREE_TYPE.ANON
        log.info(f'Canonicalized trees was selected')
        return canon_edits, TREE_TYPE.CANON

    def apply_diffs(self, edits: List[ChangeVector], tree_type: TREE_TYPE = TREE_TYPE.CANON) -> ast.AST:
        source_tree = deepcopy(self._orig_source_tree)
        if len(edits) == 0:
            return source_tree

        if tree_type == TREE_TYPE.ANON:
            current_source_tree = self._anon_source_tree
        elif tree_type == TREE_TYPE.CANON:
            current_source_tree = self._canon_source_tree
        else:
            raise ValueError
            # Todo: raise correct error
            pass
        edits = mapEdit(current_source_tree, source_tree, edits)
        for e in edits:
            e.start = source_tree
            source_tree = e.applyChange()
        log.info(f'Source code before applying diffs is:\n{printFunction(self._orig_source_tree)}\n'
                 f'Source code after applying diffs is:\n{printFunction(source_tree)}')
        return source_tree

