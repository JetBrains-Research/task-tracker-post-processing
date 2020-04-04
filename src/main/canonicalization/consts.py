# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from enum import Enum

class TREE_TYPE(Enum):
    ORIG = 'original',
    ANON = 'anonymized'
    CANON = 'canonicalized'

    @classmethod
    def get_all_types_set(cls):
        return {t for t in cls}