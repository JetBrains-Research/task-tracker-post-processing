# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Dict


class IdCounter:
    _instances: Dict[str, int] = {}
    _last_id = 0

    def __init__(self, class_name: str):
        self.__class__._instances[class_name] = self.__class__._instances.get(class_name, 0)
        self._id = self.__class__._instances.get(class_name)
        self.__class__._instances[class_name] += 1

    @property
    def id(self) -> int:
        return self._id

    @staticmethod
    def reset():
        IdCounter._instances = {}
