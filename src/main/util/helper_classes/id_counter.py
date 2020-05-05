# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from collections import defaultdict
from typing import Dict, Any, Optional, Type

from src.main.util.consts import LOGGER_NAME
from src.main.util.log_util import log_and_raise_error

log = logging.getLogger(LOGGER_NAME)


class IdCounter:
    _instances: Dict[str, int] = defaultdict(int)
    _id_item_dict_by_class: Dict[str, Dict[int, Any]] = defaultdict(lambda: defaultdict(lambda: None))
    _last_id = 0

    def __init__(self, to_store_items: bool = False):
        self._id = self.__class__._instances[self.__class__.__name__]
        self.id_item_dict_by_class = defaultdict(lambda: None)
        if to_store_items:
            self.__class__._id_item_dict_by_class[self.__class__.__name__][self._id] = self
        self.__class__._instances[self.__class__.__name__] += 1

    @property
    def id(self) -> int:
        return self._id

    @staticmethod
    def reset_all():
        IdCounter._instances = defaultdict(int)

    @classmethod
    def get_item_by_id(cls: Type['IdCounter'], id: int) -> Any:
        item = cls._id_item_dict_by_class[cls.__name__][id]
        if item is None:
            log_and_raise_error(f'Item with id {id} does not exist in the class {cls.__name__}', log)
        return item
