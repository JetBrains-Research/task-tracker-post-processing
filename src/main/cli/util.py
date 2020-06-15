# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
import argparse
from abc import ABCMeta, abstractmethod

from src.main.util import consts
from src.main.util.file_util import add_slash
from src.main.cli.configs import ALGO_LEVEL, PREPROCESSING_LEVEL
from src.main.util.consts import TASK, TRUE_VALUES_SET, FALSE_VALUES_SET
from src.main.util.log_util import configure_logger, log_and_raise_error


class ICli(object, metaclass=ABCMeta):
    description = 'Coding Assistant project.'

    def __init__(self):
        self._parser = argparse.ArgumentParser(description=self.description)
        self._log = logging.getLogger(consts.LOGGER_NAME)
        configure_logger(to_delete_previous_logs=True)
        self.configure_args()

    @abstractmethod
    def configure_args(self) -> None:
        raise NotImplemented

    @abstractmethod
    def parse_args(self) -> None:
        raise NotImplemented

    @abstractmethod
    def main(self) -> None:
        raise NotImplemented

    @classmethod
    def str_to_bool(cls, value: any) -> bool:
        if isinstance(value, bool):
            return value
        if value.lower() in FALSE_VALUES_SET:
            return False
        elif value.lower() in TRUE_VALUES_SET:
            return True
        raise argparse.ArgumentTypeError(f'{value} is not a valid boolean value')

    def str_to_task(self, task: str) -> TASK:
        try:
            return TASK(task)
        except ValueError:
            log_and_raise_error(f'Task value has to be one from the values: {TASK.tasks_values()}', self._log)

    @classmethod
    def str_to_algo_level(cls, level: str) -> ALGO_LEVEL:
        message = f'Algo level has to be an integer number from {ALGO_LEVEL.min_value()} ' \
                  f'to {ALGO_LEVEL.max_value()}'
        try:
            level = int(level)
            return ALGO_LEVEL(level)
        except ValueError:
            raise argparse.ArgumentTypeError(message)

    @classmethod
    def str_to_preprocessing_level(cls, level: str) -> PREPROCESSING_LEVEL:
        message = f'Preprosessing level has to be an integer number from {PREPROCESSING_LEVEL.min_value()} ' \
                  f'to {PREPROCESSING_LEVEL.max_value()}'
        try:
            level = int(level)
            return PREPROCESSING_LEVEL(level)
        except ValueError:
            raise argparse.ArgumentTypeError(message)

    def handle_path(self, path: str, to_add_slash: bool = True) -> str:
        if not os.path.exists(path):
            log_and_raise_error(f'Path {path} is incorrect', self._log)
        if to_add_slash:
            path = add_slash(path)
        return path

