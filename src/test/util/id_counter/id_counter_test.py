# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Type

import pytest

from src.test.util import to_skip, TEST_LEVEL
from src.main.util.id_counter import IdCounter


class A(IdCounter):
    pass


class B(IdCounter):
    pass


def get_last_id_from_id_counter(class_name: str) -> int:
    return IdCounter._instances.get(class_name, 0)


def run_reset_all_test_for_class(current_class: Type[IdCounter]) -> None:
    IdCounter.reset_all()
    o = current_class()
    assert o.id == 0
    IdCounter.reset_all()
    assert get_last_id_from_id_counter(current_class.__name__) == 0


def run_id_setting_test_for_class(current_class: Type[IdCounter]) -> None:
    o = current_class()
    assert get_last_id_from_id_counter(current_class.__name__) == o.id + 1


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.UTIL), reason=TEST_LEVEL.UTIL.value)
class TestIdCounter:

    @staticmethod
    def is_first_test(test_index: int) -> bool:
        return test_index == 0

    @pytest.mark.parametrize('i', range(10))
    def test_id_setting(self, i: int) -> None:
        if self.__class__.is_first_test(i):
            # Before all tests
            IdCounter.reset_all()
        run_id_setting_test_for_class(A)
        run_id_setting_test_for_class(B)

    @pytest.mark.parametrize('i', range(10))
    def test_reset(self, i: int):
        if self.__class__.is_first_test(i):
            # Before all tests
            IdCounter.reset_all()
        a = A()
        assert a.id == 0
        IdCounter.reset(A.__name__)
        assert get_last_id_from_id_counter(A.__name__) == 0
        b = B()
        assert b.id + 1 == get_last_id_from_id_counter(B.__name__)

    @pytest.mark.parametrize('i', range(10))
    def test_reset_all(self, i: int):
        run_reset_all_test_for_class(A)
        run_reset_all_test_for_class(B)
