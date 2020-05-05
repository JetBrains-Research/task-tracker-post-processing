# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Type

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.helper_classes.id_counter import IdCounter


class A(IdCounter):
    pass


class B(IdCounter):
    pass


class C(IdCounter):
    def __init__(self):
        super().__init__(self)


def get_last_id_from_id_counter(class_name: str) -> int:
    return IdCounter._instances[class_name]


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
    def test_reset_all(self, i: int):
        run_reset_all_test_for_class(A)
        run_reset_all_test_for_class(B)

    def test_empty_id_from_item_dict(self):
        IdCounter.reset_all()
        a = A()
        with pytest.raises(ValueError):
            A.get_item_by_id(a.id)

    def test_getting_item_by_id(self):
        IdCounter.reset_all()
        c = C()
        item = C.get_item_by_id(c.id)
        assert c == item
