# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging
import tempfile
from subprocess import check_output, CalledProcessError, STDOUT
from threading import Lock

from src.main.util import consts
from src.main.util.log_util import log_and_raise_error
from src.main.util.consts import UTF_ENCODING, EXTENSION
from src.main.canonicalization.canonicalization import get_code_from_tree

log = logging.getLogger(consts.LOGGER_NAME)

lock = Lock()

# Using GumTreeDiff: https://github.com/GumTreeDiff/gumtree/tree/master
class GumTreeDiff:

    @staticmethod
    def get_diffs_number(src_file: str, dst_file: str) -> int:
        log.info('Calling GumTreeDiff')
        try:
            args = [consts.GUMTREE_PATH, 'diffn', src_file, dst_file]
            output = check_output(args, text=True, stderr=STDOUT).strip('\n')
            return int(output)
        except CalledProcessError as e:
            log_and_raise_error(f'Error during GumTreeDiff running: {e}, src: {src_file}, dst: {dst_file}', log)
            exit(1)

    @staticmethod
    def create_tmp_files_and_get_diffs_number(src_tree: ast.AST, dst_tree: ast.AST) -> int:
        # Todo: make it better
        with tempfile.NamedTemporaryFile(suffix=EXTENSION.PY.value) as src_file, \
                tempfile.NamedTemporaryFile(suffix=EXTENSION.PY.value) as dst_file:
            src_file.write(bytes(get_code_from_tree(src_tree), encoding=UTF_ENCODING))
            dst_file.write(bytes(get_code_from_tree(dst_tree), encoding=UTF_ENCODING))
            dst_file.seek(0)
            src_file.seek(0)

            return GumTreeDiff.get_diffs_number(src_file.name, dst_file.name)
