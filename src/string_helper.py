def count_containing_substring(list_of_string: list, substring: str):
    count = 0
    for i, s in enumerate(list_of_string):
        if substring in s:
            count += 1
    return count


def index_containing_substring(list_of_string: list, substring: str):
    for i, s in enumerate(list_of_string):
        if substring in s:
            return i
    return -1
