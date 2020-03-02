import re


def does_string_contain_any_of_substrings(string: str, substrings: list):
    for substring in substrings:
        if substring in string:
            return True
    return False


def convert_camel_case_to_snake_case(string: str):
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$|_)|\d+', string)
    return '_'.join(map(str.lower, words))
