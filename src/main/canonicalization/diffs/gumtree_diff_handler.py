# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging
import tempfile
from typing import Optional
from subprocess import check_output, CalledProcessError, STDOUT

from src.main.util import consts
from src.main.util.log_util import log_and_raise_error
from src.main.util.consts import UTF_ENCODING, EXTENSION
from src.main.canonicalization.diffs.diff_handler import IDiffHandler
from src.main.canonicalization.canonicalization import get_code_from_tree

log = logging.getLogger(consts.LOGGER_NAME)


# Todo: do we need a class with two static methods and implementation of base class method, that's unused?
# Using GumTreeDiff: https://github.com/GumTreeDiff/gumtree/tree/master
class GumTreeDiffHandler(IDiffHandler):

    @staticmethod
    def get_diffs_number_with_gumtree(src_file: str, dst_file: str) -> int:
        try:
            args = ['ls', '/tmp']
            output = check_output(args, text=True, stderr=STDOUT).strip('\n')
            print(output + '\n\n\n')
            args = [consts.GUMTREE_PATH, 'diffn', src_file, dst_file]
            output = check_output(args, text=True, stderr=STDOUT).strip('\n')
            print(f'Output: {output}')
            return int(output)
        except CalledProcessError as e:
            args = ['ls', '/tmp']
            output = check_output(args, text=True, stderr=STDOUT).strip('\n')
            print(output + '\n\n\n')
            log_and_raise_error(f'Error during GumTreeDiff running: {e}, src file: {src_file}, dst file: {dst_file}',
                                log, ValueError)
            exit(1)

    @staticmethod
    def create_tmp_files_and_run_gumtree(src_tree: ast.AST, dst_tree: ast.AST) -> int:
        # Todo: make it better
        with tempfile.NamedTemporaryFile(suffix=EXTENSION.PY.value) as src_file, \
                tempfile.NamedTemporaryFile(suffix=EXTENSION.PY.value) as dst_file:
            src_file.write(bytes(get_code_from_tree(src_tree), encoding=UTF_ENCODING))
            dst_file.write(bytes(get_code_from_tree(dst_tree), encoding=UTF_ENCODING))
            dst_file.seek(0)
            src_file.seek(0)

            return GumTreeDiffHandler.get_diffs_number_with_gumtree(src_file.name, dst_file.name)

    # We don't use this method anymore, so maybe it's better to get rid of it and this base class?
    def get_diffs_number(self, anon_dst_tree: Optional[ast.AST], canon_dst_tree: Optional[ast.AST]) -> int:
        if anon_dst_tree is None and canon_dst_tree is None:
            log_and_raise_error(f'Both trees cannot be empty!', log)

        diffs_number = []
        if anon_dst_tree is not None:
            diffs_number.append(self.__class__.create_tmp_files_and_run_gumtree(self._anon_tree, anon_dst_tree))
        if canon_dst_tree is not None:
            diffs_number.append(self.__class__.create_tmp_files_and_run_gumtree(self._canon_tree, canon_dst_tree))

        return min(diffs_number)
