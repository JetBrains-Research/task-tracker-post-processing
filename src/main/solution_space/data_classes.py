# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast

from typing import List
from src.main.util import consts
from src.main.canonicalization.canonicalization import get_code_from_tree


class AtiItem:
    def __init__(self, timestamp=0, event_type=None, event_data=None):
        self._timestamp = timestamp
        self._event_type = event_type
        self._event_data = event_data

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def event_type(self) -> consts.ACTIVITY_TRACKER_EVENTS:
        return self._event_type

    @property
    def event_data(self) -> consts.ACTIVITY_TRACKER_EVENTS:
        return self._event_data

    def is_empty(self) -> bool:
        return self._timestamp == 0 and self._event_type is None and self._event_data is None


class Profile:
    def __init__(self, age=consts.DEFAULT_VALUES.AGE.value, experience=consts.DEFAULT_VALUES.EXPERIENCE.value):
        self._age = age
        self._experience = experience

    @property
    def age(self) -> int:
        return self._age

    # Todo: add enum??
    @property
    def experience(self) -> str:
        return self._experience


class User:
    def __init__(self, profile=None, timestamp=0, date=None, ati_actions=None):
        # Todo: add id
        self._profile = profile
        self._ati_actions = []
        if ati_actions is not None:
            self._ati_actions = ati_actions
        self._timestamp = timestamp
        self._date = date

    @property
    def profile(self) -> Profile:
        return self._profile

    @property
    def ati_actions(self) -> List[AtiItem]:
        return self._ati_actions

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def date(self) -> str:
        return self._date


class Code:
    def __init__(self, ast=None, rate=0.0):
        self._ast = ast
        self._rate = rate

    @property
    def ast(self) -> ast.AST:
        return self._ast

    @property
    def rate(self) -> float:
        return self._rate

    def __str__(self) -> str:
        return f'Rate: {self._rate}\nCode:\n{get_code_from_tree(self._ast)}\n'


