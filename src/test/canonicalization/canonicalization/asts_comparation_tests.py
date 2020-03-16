import ast
import logging
import unittest

from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT
from src.main.canonicalization.canonicalization import are_asts_equal, get_code_from_tree


empty_source = ''

source_0 = \
    'def main():\n' \
    '    n = int(input())\n' \
    '    l = []\n' \
    '    for i in range(n):\n' \
    '        l.append(int(input()))\n' \
    '    if 0 in l:\n' \
    '        print("YES")\n' \
    '    else:\n' \
    '        print("NO")\n' \
    'if __name__ == "__main__":\n    main()'

#  print("NO") ->  print("NOO")
source_1 =  \
    'def main():\n' \
    '    n = int(input())\n' \
    '    l = []\n' \
    '    for i in range(n):\n' \
    '        l.append(int(input()))\n' \
    '    if 0 in l:\n' \
    '        print("YES")\n' \
    '    else:\n' \
    '        print("NOO")\n' \
    'if __name__ == "__main__":\n    main()'

# n = int(input()) -> n = (input())
source_2 =  \
    'def main():\n' \
    '    n = (input())\n' \
    '    l = []\n' \
    '    for i in range(n):\n' \
    '        l.append(int(input()))\n' \
    '    if 0 in l:\n' \
    '        print("YES")\n' \
    '    else:\n' \
    '        print("NO")\n' \
    'if __name__ == "__main__":\n    main()'

# l = [] -> l = {}
source_3 =  \
    'def main():\n' \
    '    n = int(input())\n' \
    '    l = {}\n' \
    '    for i in range(n):\n' \
    '        l.append(int(input()))\n' \
    '    if 0 in l:\n' \
    '        print("YES")\n' \
    '    else:\n' \
    '        print("NO")\n' \
    'if __name__ == "__main__":\n    main()'


# if 0 in l: -> if 1 in l:
source_4 = \
    'def main():\n' \
    '    n = int(input())\n' \
    '    l = []\n' \
    '    for i in range(n):\n' \
    '        l.append(int(input()))\n' \
    '    if 1 in l:\n' \
    '        print("YES")\n' \
    '    else:\n' \
    '        print("NO")\n' \
    'if __name__ == "__main__":\n    main()'

# it shouldn't change ast
# print("YES") ->  print(\'YES\')
source_5 = \
    'def main():\n' \
    '    n = int(input())\n' \
    '    l = []\n' \
    '    for i in range(n):\n' \
    '        l.append(int(input()))\n' \
    '    if 0 in l:\n' \
    '        print(\'YES\')\n' \
    '    else:\n' \
    '        print("NO")\n' \
    'if __name__ == "__main__":\n    main()'

# it shouldn't change ast
# if 0 in l: -> if (0 in l):
source_6 = \
    'def main():\n' \
    '    n = int(input())\n' \
    '    l = []\n' \
    '    for i in range(n):\n' \
    '        l.append(int(input()))\n' \
    '    if (0 in l):\n' \
    '        print("YES")\n' \
    '    else:\n' \
    '        print("NO")\n' \
    'if __name__ == "__main__":\n    main()'

sources_without_empty = [source_0, source_1, source_2, source_3, source_4, source_5, source_6]
sources_with_empty = sources_without_empty + [empty_source]
different_sources = [source_0, source_1, source_2, source_3, source_4]
equal_sources = [source_0, source_5, source_6]


def get_asts_from_sources(sources):
    return [ast.parse(source) for source in sources]


class TestASTsComparation(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_same_ast(self) -> None:
        asts = get_asts_from_sources(sources_with_empty)
        for ast in asts:
            self.assertTrue(are_asts_equal(ast, ast))

    def test_empty_ast(self) -> None:
        not_empty_asts = get_asts_from_sources(sources_without_empty)
        empty_ast_1 = ast.parse('')
        empty_ast_2 = ast.parse('')
        # check that different empty asts are equal
        self.assertTrue(are_asts_equal(empty_ast_1, empty_ast_2))

        for not_empty_ast in not_empty_asts:
            self.assertFalse(are_asts_equal(empty_ast_1, not_empty_ast), f'\n\n{get_code_from_tree(empty_ast_1)} \n\n\n{get_code_from_tree(not_empty_ast)}')

    def test_different_asts(self) -> None:
        asts = get_asts_from_sources(different_sources)
        for i in range(len(asts)):
            for j in range(i + 1, len(asts)):
                self.assertFalse(are_asts_equal(asts[i], asts[j]), f'\nast {i}: \n{get_code_from_tree(asts[i])} \n\n\nast {j}: {get_code_from_tree(asts[j])}')

    def test_equal_asts(self) -> None:
        asts = get_asts_from_sources(equal_sources)
        for i in range(len(asts)):
            for j in range(i + 1, len(asts)):
                self.assertTrue(are_asts_equal(asts[i], asts[j]), f'\nast {i}: \n{get_code_from_tree(asts[i])} \n\n\nast {j}: {get_code_from_tree(asts[j])}')
