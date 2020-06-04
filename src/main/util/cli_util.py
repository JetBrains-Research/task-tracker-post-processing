# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import argparse
from abc import ABCMeta, abstractmethod

from src.main.util import consts
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

    def get_task(self, task: str) -> TASK:
        try:
            return TASK(task)
        except ValueError:
            log_and_raise_error(f'Task value has to be one from the values: {TASK.tasks_values()}', self._log)
