# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import numpy as np
from datetime import datetime

from typing import List, Union
from src.main.util import consts
from src.main.canonicalization.canonicalization import get_code_from_tree
from src.main.util.consts import EXPERIENCE, DEFAULT_VALUES, ACTIVITY_TRACKER_EVENTS


class AtiItem:
    def __init__(self, timestamp: datetime = DEFAULT_VALUES.DATE.value,
                 event_type: Union[ACTIVITY_TRACKER_EVENTS, DEFAULT_VALUES] = DEFAULT_VALUES.EVENT_TYPE,
                 event_data: str = DEFAULT_VALUES.EVENT_DATA.value):
        self._timestamp = timestamp
        self._event_type = event_type
        self._event_data = event_data

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def event_type(self) -> Union[ACTIVITY_TRACKER_EVENTS, DEFAULT_VALUES]:
        return self._event_type

    @property
    def event_data(self) -> str:
        return self._event_data

    def is_empty(self) -> bool:
        return DEFAULT_VALUES.DATE.is_equal(self._timestamp) and DEFAULT_VALUES.EVENT_DATA.is_equal(self._event_type.value)\
               and DEFAULT_VALUES.EVENT_DATA.is_equal(self._event_data)

    def __str__(self) -> str:
        return f'Timestamp: {self._timestamp}, event_type: {self._event_type.value}, event_data: {self._event_data}'


class Profile:
    def __init__(self, age: int = consts.DEFAULT_VALUES.AGE.value,
                 experience: Union[EXPERIENCE, DEFAULT_VALUES] = DEFAULT_VALUES.EXPERIENCE):
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

    def __init__(self, profile: Profile = None):
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
    def __init__(self, user: User, timestamp: int = 0, date: datetime = DEFAULT_VALUES.DATE.value,
                 ati_actions: List[AtiItem] = None):
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
    def date(self) -> timestamp:
        return self._date


class Code:
    def __init__(self, ast: ast.AST = None, rate: float = 0.0):
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

