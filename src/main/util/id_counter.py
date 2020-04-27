# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Dict
from collections import defaultdict


class IdCounter:
    _instances: Dict[str, int] = defaultdict(int)
    _last_id = 0

    def __init__(self):
        self._id = self.__class__._instances.get(self.__class__.__name__, 0)
        self.__class__._instances[self.__class__.__name__] += 1

    @property
    def id(self) -> int:
        return self._id

    @staticmethod
    def reset_all():
        IdCounter._instances = defaultdict(int)

    @staticmethod
    def reset(class_name: str):
        IdCounter._instances[class_name] = 0
