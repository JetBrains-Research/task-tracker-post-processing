# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
import logging
from datetime import datetime
from typing import List, Union, Optional

from src.main.util import consts
from src.main.util.consts import EXPERIENCE, DEFAULT_VALUE, ACTIVITY_TRACKER_EVENTS

log = logging.getLogger(consts.LOGGER_NAME)


class AtiItem:
    def __init__(self, timestamp: datetime = DEFAULT_VALUE.DATE.value,
                 event_type: Union[ACTIVITY_TRACKER_EVENTS, DEFAULT_VALUE] = DEFAULT_VALUE.EVENT_TYPE,
                 event_data: str = DEFAULT_VALUE.EVENT_DATA.value):
        self._timestamp = timestamp
        self._event_type = event_type
        self._event_data = event_data

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def event_type(self) -> Union[ACTIVITY_TRACKER_EVENTS, DEFAULT_VALUE]:
        return self._event_type

    @property
    def event_data(self) -> str:
        return self._event_data

    # Todo: add tests
    def is_empty(self) -> bool:
        return DEFAULT_VALUE.DATE.is_equal(self._timestamp) and DEFAULT_VALUE.EVENT_DATA.is_equal(
            self._event_type.value) \
               and DEFAULT_VALUE.EVENT_DATA.is_equal(self._event_data)

    def __str__(self) -> str:
        return f'Timestamp: {self._timestamp}, event_type: {self._event_type}, event_data: {self._event_data}'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, AtiItem):
            return False
        return self._timestamp == o._timestamp and \
               self._event_type == o._event_type and \
               self._event_data == o._event_data


class Profile:
    def __init__(self, age: int = consts.DEFAULT_VALUE.AGE.value,
                 experience: Union[EXPERIENCE, DEFAULT_VALUE] = DEFAULT_VALUE.EXPERIENCE):
        self._age = age
        self._experience = experience

    @property
    def age(self) -> int:
        return self._age

    @property
    def experience(self) -> Union[EXPERIENCE, DEFAULT_VALUE]:
        return self._experience

    def __str__(self) -> str:
        return f'Experience: {self._experience}, age: {self._age}'


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

    def __str__(self) -> str:
        return f'Id: {self._id}, profile: {self._profile}'


class CodeInfo:
    def __init__(self, user: User, timestamp: int = 0, date: datetime = DEFAULT_VALUE.DATE.value,
                 ati_actions: Optional[List[AtiItem]] = None):
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

    def __str__(self) -> str:
        return f'User: {self._user}, timestamp: {self._timestamp}, date: {self._date}. ' \
               f'Length of ati actions is {len(self._ati_actions)}'
