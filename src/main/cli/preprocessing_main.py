# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os

from src.main.util.cli_util import ICli
from src.main.util.consts import FILE_SYSTEM_ITEM
from src.main.util.configs import PREPROCESSING_LEVEL
from src.main.util.log_util import log_and_raise_error
from src.main.splitting.tasks_tests_handler import run_tests
from src.main.preprocessing.preprocessing import preprocess_data
from src.main.splitting.splitting import split_tasks_into_separate_files
from src.main.preprocessing.int_experience_adding import add_int_experience
from src.main.preprocessing.intermediate_diffs_removing import remove_intermediate_diffs
from src.main.preprocessing.inefficient_statements_removing import remove_inefficient_statements
from src.main.util.file_util import add_slash, get_all_file_system_items, language_item_condition


class PreprocessingCli(ICli):

    def __init__(self):
        super().__init__()
        self._path = None
        self._level = None

    def configure_args(self) -> None:
        self._parser.add_argument('path', type=str, nargs=1, help='data path')
        self._parser.add_argument('--level', nargs='?', const=PREPROCESSING_LEVEL.max_value(),
                                  default=PREPROCESSING_LEVEL.max_value(),
                                  help=PREPROCESSING_LEVEL.description())

    def parse_args(self) -> None:
        args = self._parser.parse_args()
        path = args.path[0]
        if not os.path.exists(args.path[0]):
            log_and_raise_error(f'Path {path} does not exist', self._log)
        path = add_slash(path)
        self._path = path
        self._level = PREPROCESSING_LEVEL.get_level(args.level)

    def main(self) -> None:
        self.parse_args()
        preprocessing_functions = [preprocess_data, run_tests, split_tasks_into_separate_files,
                                   remove_intermediate_diffs, remove_inefficient_statements,
                                   add_int_experience]
        paths = [self._path]
        for function_index in range(0, self._level.value + 1):
            self._log.info(f'Current operation is {preprocessing_functions[function_index]}')
            new_paths = []
            for path in paths:
                path = preprocessing_functions[function_index](path)
                if function_index == PREPROCESSING_LEVEL.TESTS_RESULTS.value:
                    # Get all sub folders
                    new_paths += get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
                else:
                    new_paths.append(path)
            paths = list(new_paths)

        str_paths = '\n'.join(paths)
        self._log.info(f'Folders with data: {str_paths}')
        print(f'Folders with data: {str_paths}')


if __name__ == '__main__':
    preprocessing_cli = PreprocessingCli()
    preprocessing_cli.main()
