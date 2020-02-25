def does_string_contain_any_of_substrings(string: str, substrings: list):
    for substring in substrings:
        if substring in string:
            return True
    return False
