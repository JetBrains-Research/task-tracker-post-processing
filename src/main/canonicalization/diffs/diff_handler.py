# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging
from abc import ABCMeta, abstractmethod
from typing import Optional

from src.main.util import consts
from src.main.canonicalization.consts import TREE_TYPE
from src.main.canonicalization.canonicalization import get_trees

log = logging.getLogger(consts.LOGGER_NAME)


class IDiffHandler(object, metaclass=ABCMeta):
    def __init__(self, source_code: Optional[str] = None,
                 anon_tree: Optional[ast.AST] = None,
                 canon_tree: Optional[ast.AST] = None):
        if source_code is not None:
            self._orig_tree, self._anon_tree, self._canon_tree = get_trees(source_code, TREE_TYPE.get_all_types_set())
        else:
            self._orig_tree, self._anon_tree, self._canon_tree = None, anon_tree, canon_tree

    @property
    def orig_tree(self) -> ast.AST:
        return self._orig_tree

    @property
    def anon_tree(self) -> ast.AST:
        return self._anon_tree

    @property
    def canon_tree(self) -> ast.AST:
        return self._canon_tree

    @abstractmethod
    def get_diffs_number(self, anon_dst_tree: Optional[ast.AST], canon_dst_tree: Optional[ast.AST]) -> int:
        raise NotImplementedError

    def get_diffs_number_from_diff_handler(self, diff_handler: 'IDiffHandler') -> int:
        return self.get_diffs_number(diff_handler.anon_tree, diff_handler.canon_tree)
