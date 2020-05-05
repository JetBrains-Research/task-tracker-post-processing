# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

"""
  We need the util because the pickle module cannot serialize/deserialize defaultdict with lambda functions
"""

from collections import defaultdict


def get_none() -> None:
    return None


def get_empty_list() -> list:
    return []


def get_default_dict_with_default_dict_with_none() -> dict:
    return defaultdict(get_none())
