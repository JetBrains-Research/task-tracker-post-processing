# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import os
import ast
import logging
from typing import List, Dict, Callable, Optional

from src.main.util import consts
from src.main.util.consts import TASK
from src.main.util.log_util import log_and_raise_error
from src.main.canonicalization.consts import TREE_TYPE
from src.main.util.file_util import create_file, is_file
from src.main.util.helper_classes.id_counter import IdCounter
from src.main.util.language_util import get_extension_by_language
from src.main.util.helper_classes.pretty_string import PrettyString
from src.main.splitting.tasks_tests_handler import check_tasks, create_in_and_out_dict
from src.main.canonicalization.canonicalization import are_asts_equal, get_code_from_tree, get_trees

log = logging.getLogger(consts.LOGGER_NAME)


class Code(PrettyString):

    def __init__(self, anon_tree: ast.AST, canon_tree: ast.AST, rate: float,
                 language: consts.LANGUAGE = consts.LANGUAGE.PYTHON):
        self._canon_tree = canon_tree
        self._rate = rate
        self._anon_tree = anon_tree
        self._language = language

    @classmethod
    def from_source(cls, source: str, rate: Optional[float], task: Optional[TASK] = None,
                    language: consts.LANGUAGE = consts.LANGUAGE.PYTHON) -> Code:
        anon_tree, canon_tree = get_trees(source, {TREE_TYPE.ANON, TREE_TYPE.CANON})
        if rate is None:
            if task is None:
                log_and_raise_error('Cannot find rate without task: both are None', log)
            rate = check_tasks([task], source, create_in_and_out_dict([task]), language)[0]
        return Code(anon_tree, canon_tree, rate, language)

    @property
    def canon_tree(self) -> ast.AST:
        return self._canon_tree

    @property
    def anon_tree(self) -> ast.AST:
        return self._anon_tree

    @property
    def rate(self) -> float:
        return self._rate

    @property
    def language(self) -> consts.LANGUAGE:
        return self._language

    def __str__(self) -> str:
        return f'Rate: {self._rate}\nLanguage: {self._language.value}\n' \
               f'Canon tree:\n{get_code_from_tree(self._canon_tree)}\n' \
               f'Anon tree:\n{get_code_from_tree(self.anon_tree)}\n'


class SerializedCode(IdCounter, PrettyString):

    def __init__(self, anon_tree: ast.AST, canon_tree: ast.AST, rate: float, folder_with_files: str, file_prefix: str,
                 language: consts.LANGUAGE = consts.LANGUAGE.PYTHON):
        super().__init__()
        self._anon_trees = [anon_tree]
        self._canon_tree = canon_tree
        self._rate = rate
        self._folder_with_files = folder_with_files
        self._file_prefix = file_prefix
        self._language = language

        # files for each tree are stored in dict
        self._file_by_tree_dict: Dict[ast.AST, str] = {}
        self.__create_files_for_trees()

    @classmethod
    def from_code(cls, code: Code, folder_with_files: str, file_prefix: str) -> SerializedCode:
        return SerializedCode(code.anon_tree, code.canon_tree, code.rate, folder_with_files, file_prefix, code.language)


    @property
    def canon_tree(self) -> ast.AST:
        return self._canon_tree

    @property
    def anon_trees(self) -> List[ast.AST]:
        return self._anon_trees

    @property
    def rate(self) -> float:
        return self._rate

    @property
    def language(self) -> consts.LANGUAGE:
        return self._language

    def is_full(self) -> bool:
        return self._rate == consts.TEST_RESULT.FULL_SOLUTION.value

    def add_anon_tree(self, anon_tree) -> Optional[str]:
        if self.__does_contain_anon_tree(anon_tree):
            return None

        self._anon_trees.append(anon_tree)
        index_of_tree = self._anon_trees.index(anon_tree)
        return self.__create_file_for_tree(anon_tree, f'{TREE_TYPE.ANON.value}_{index_of_tree}')

    def get_anon_files(self, filter_anon_trees: Callable[[ast.AST], bool] = (lambda tree: True)) -> List[str]:
        anon_tree_files = []
        for anon_tree in list(filter(filter_anon_trees, self._anon_trees)):
            anon_tree_files.append(self.__get_file_by_tree(anon_tree))
        return anon_tree_files

    def get_canon_file(self) -> str:
        return self.__get_file_by_tree(self._canon_tree)

    def recreate_files_for_trees(self, new_folder_with_files: str) -> None:
        self._folder_with_files = new_folder_with_files
        self.__create_files_for_trees(to_rewrite=True)

    def __create_files_for_trees(self, to_rewrite: bool = False) -> None:
        self.__create_file_for_tree(self._canon_tree, TREE_TYPE.CANON.value, to_overwrite=to_rewrite)
        for i, anon_tree in enumerate(self._anon_trees):
            self.__create_file_for_tree(anon_tree, f'{TREE_TYPE.ANON.value}_{i}', to_overwrite=to_rewrite)

    # If file exists already in graph folder, we don't want to override it
    def __create_file_for_tree(self, tree: ast.AST, str_tree_type: str,
                               to_overwrite: bool = False) -> str:
        if self._file_by_tree_dict.get(tree) is not None and not to_overwrite:
            log_and_raise_error(f'File for tree {get_code_from_tree(tree)} already exists in files dict', log)

        extension = get_extension_by_language(self._language)
        file_path = os.path.join(self._folder_with_files,
                                 f'{self._file_prefix}_{str(self._id)}_{str_tree_type}{str(extension.value)}')

        if not is_file(file_path):
            code = get_code_from_tree(tree)
            create_file(code, file_path)

        self._file_by_tree_dict[tree] = file_path
        return file_path

    def __does_contain_anon_tree(self, anon_tree: ast.AST) -> bool:
        for a_t in self._anon_trees:
            if are_asts_equal(a_t, anon_tree):
                return True
        return False

    def __get_file_by_tree(self, tree: ast.AST) -> str:
        tree_file = self._file_by_tree_dict[tree]
        if tree_file is None:
            log_and_raise_error(f'No file is created for anon_tree {get_code_from_tree(tree)}', log)
        return tree_file

    def __str__(self) -> str:
        return f'Id: {self._id}\n' \
               f'Rate: {self._rate}\n' \
               f'Language: {self._language.value}\n' \
               f'Canon tree:\n{get_code_from_tree(self._canon_tree)}\nAnon trees:' \
               f'{list(map(lambda tree: get_code_from_tree(tree), self._anon_trees))}\n'
