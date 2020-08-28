# Copyright (c) by anonymous author(s)

import sys
import logging

sys.path.append('.')
from src.main.util import consts
from src.main.cli.util import ICli
from src.main.util.consts import FILE_SYSTEM_ITEM
from src.main.cli.configs import PREPROCESSING_LEVEL, PREPROCESSING_PARAMS
from src.main.util.log_util import configure_logger, add_console_stream
from src.main.util.file_util import get_all_file_system_items, language_item_condition

log = logging.getLogger(consts.LOGGER_NAME)


class PreprocessingCli(ICli):

    def __init__(self):
        super().__init__()
        self._path = None
        self._level = None

    def configure_args(self) -> None:
        self._parser.add_argument(PREPROCESSING_PARAMS.PATH.value, type=str, nargs=1, help='data path')
        self._parser.add_argument(PREPROCESSING_PARAMS.LEVEL.value, nargs='?', const=PREPROCESSING_LEVEL.max_value(),
                                  default=PREPROCESSING_LEVEL.max_value(),
                                  help=PREPROCESSING_LEVEL.description())

    def parse_args(self) -> None:
        args = self._parser.parse_args()
        self._path = self.handle_path(args.path[0])
        self._level = self.str_to_preprocessing_level(args.level)

    def main(self) -> None:
        self.parse_args()
        paths = [self._path]
        for level_index in range(0, self._level.value + 1):
            current_level = PREPROCESSING_LEVEL(level_index)
            self._log.info(f'Current action is {current_level.level_handler()}')
            new_paths = []
            for path in paths:
                path = current_level.level_handler()(path)
                if current_level == PREPROCESSING_LEVEL.TESTS_RESULTS:
                    # Get all sub folders
                    new_paths += get_all_file_system_items(path, language_item_condition, FILE_SYSTEM_ITEM.SUBDIR)
                else:
                    new_paths.append(path)
            paths = list(new_paths)

        str_paths = '\n'.join(paths)
        self._log.info(f'Folders with data: {str_paths}')
        print(f'Folders with data: {str_paths}')


if __name__ == '__main__':
    configure_logger(to_delete_previous_logs=True)
    add_console_stream(log)

    preprocessing_cli = PreprocessingCli()
    preprocessing_cli.main()
