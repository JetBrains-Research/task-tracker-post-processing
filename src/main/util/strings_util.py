# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import re

def does_string_contain_any_of_substrings(string: str, substrings: list):
    for substring in substrings:
        if substring in string:
            return True
    return False


def convert_camel_case_to_snake_case(string: str):
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$|_)|\d+', string)
    return '_'.join(map(str.lower, words))


def crop_string(string: str, short_part_length: int, separator='...'):
    return ''.join((string[:short_part_length], separator, string[-short_part_length:]))
