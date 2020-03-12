# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina


from src.main.util import consts


class AtiItem:
    def __init__(self, timestamp=0, event_type=None, event_data=None):
        self._timestamp = timestamp
        self._event_type = event_type
        self._event_data = event_data

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def event_type(self):
        return self.event_type

    @property
    def event_data(self):
        return self.event_data


class Profile:
    def __init__(self, age=consts.DEFAULT_VALUES.AGE.value, experience=consts.DEFAULT_VALUES.EXPERIENCE.value):
        self._age = age
        self._experience = experience

    @property
    def age(self):
        return self._age

    @property
    def experience(self):
        return self._experience


class User:
    def __init__(self, profile=None, timestamp=0, date=None):
        # Todo: add id
        self._profile = profile
        self._ati_actions = []
        self._timestamp = timestamp
        self._date = date

    @property
    def profile(self):
        return self._profile

    @property
    def ati_actions(self):
        return self._ati_actions

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def date(self):
        return self._date


class Code:
    def __init__(self, ast=None, rate=0.0):
        self._ast = ast
        self._rate = rate

    @property
    def ast(self):
        return self._ast

    @property
    def rate(self):
        return self._rate

    # Todo: ovveride it - use print function from Kelly Rivers
    def __str__(self) -> str:
        return super().__str__()


