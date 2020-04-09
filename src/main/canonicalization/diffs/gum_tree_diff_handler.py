# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging

from src.main.util import consts
from src.main.canonicalization.diffs.diff_handler import IDiffHandler

log = logging.getLogger(consts.LOGGER_NAME)


# Use GumTreeDiff: https://github.com/GumTreeDiff/gumtree/tree/master


class GumTreeDiffHandler(IDiffHandler):

    def get_diffs_number(self, canon_tree: ast.AST) -> int:
        # Todo: run gum tree
        pass