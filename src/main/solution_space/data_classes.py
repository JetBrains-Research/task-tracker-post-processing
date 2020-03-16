# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast

from typing import List, Union
from src.main.util import consts
from src.main.canonicalization.canonicalization import get_code_from_tree
from src.main.util.consts import EXPERIENCE, DEFAULT_VALUES


class AtiItem:
    def __init__(self, timestamp: int = 0, event_type=None, event_data=None):
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
    def __init__(self, age=consts.DEFAULT_VALUES.AGE.value, experience: Union[EXPERIENCE, DEFAULT_VALUES] = DEFAULT_VALUES.EXPERIENCE):
        self._age = age
        self._experience = experience

    @property
    def age(self) -> int:
        return self._age

    @property
    def experience(self) -> Union[EXPERIENCE, DEFAULT_VALUES]:
        return self._experience


class User:
    _last_id = 0

    def __init__(self, profile=None):
        self._profile = profile
        self._id = self._last_id
        self.__class__._last_id += 1


    @property
    def profile(self) -> Profile:
        return self._profile

    @property
    def id(self) -> int:
        return self._id


class CodeInfo:
    def __init__(self, user: User, timestamp: int = 0, date: str = None, ati_actions: List[AtiItem] = None):
        self._user = user
        self._ati_actions = ati_actions if ati_actions else []
        self._timestamp = timestamp
        self._date = date

    @property
    def user(self) -> User:
        return self._user

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

    def is_full(self) -> bool:
        return self._rate == consts.TEST_RESULT.FULL_SOLUTION.value

