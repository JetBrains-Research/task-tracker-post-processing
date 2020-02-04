import logging

from src.main import tasks_tests_handler as tth, consts
import unittest

from src.main.consts import LANGUAGE




def is_equals(pair_1, pair_2):
    if pair_1[0] == pair_2[0] and pair_1[1] == pair_2[1]:
        return True
    return False


# Python tests
def get_python_code_test_data_full_solution():
    python_code = 'a = int(input())\nb = int(input())\nn = int(input())\nprint(str((a * 100 * n + b * n) // 100) + " ' \
                  '" + str((a * 100 * n + b * n) % 100)) '
    current_pair = tth.check_task('pies', python_code, language=LANGUAGE.PYTHON.value)
    return current_pair, (8, 8)


def get_python_code_test_data_partial_solution():
    python_code = 'a = int(input())\nb = int(input())\nn = int(input())\nprint(str(a * n) + " " + str((b * n)))'
    current_pair = tth.check_task('pies', python_code, language=LANGUAGE.PYTHON.value)
    return current_pair, (8, 3)


def get_python_code_test_data_not_solved_solution():
    python_code = 'a = int(input())\n'
    current_pair = tth.check_task('pies', python_code, language=LANGUAGE.PYTHON.value)
    return current_pair, (8, 0)


def get_python_code_test_data_error_solution():
    python_code = 'a = int(input())\nb = int(input()\nn = int(input())\nprint(str(a * n) + " " + str((b * n)))'
    current_pair = tth.check_task('pies', python_code, language=LANGUAGE.PYTHON.value)
    return current_pair, (8, 0)


# Java tests
def get_java_code_test_data_full_solution():
    java_code = 'import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader(System.in);\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n        System.out.println((a * n + b * n / 100) + " " + (b * n % 100));\n    }\n}'
    current_pair = tth.check_task('pies', java_code, language=LANGUAGE.JAVA.value)
    return current_pair, (8, 8)


def get_java_code_test_data_partial_solution():
    java_code = 'import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader(System.in);\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n        System.out.println(a * n + " " + b * n);\n    }\n}'
    current_pair = tth.check_task('pies', java_code, language=LANGUAGE.JAVA.value)
    return current_pair, (8, 3)


def get_java_code_test_data_not_solved_solution():
    java_code = 'import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader(System.in);\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n    }\n}'
    current_pair = tth.check_task('pies', java_code, language=LANGUAGE.JAVA.value)
    return current_pair, (8, 0)


def get_java_code_test_data_error_solution():
    java_code = 'import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader();\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n        System.out.println(a * n + " " + b * n);\n    }\n}'
    current_pair = tth.check_task('pies', java_code, language=LANGUAGE.JAVA.value)
    return current_pair, (8, 0)


# Kotlin tests
def get_kotlin_code_test_data_full_solution():
    kotlin_code = 'fun main(args: Array<String>) {\n    val a:Int = readLine()!!.toInt()\n    val b:Int = readLine()!!.toInt()\n    val n:Int = readLine()!!.toInt()\n    println("${a * n + b * n / 100} ${b * n % 100}")\n}'
    current_pair = tth.check_task('pies', kotlin_code, language=LANGUAGE.KOTLIN.value)
    return current_pair, (8, 8)


def get_kotlin_code_test_data_partial_solution():
    kotlin_code = 'fun main(args: Array<String>) {\n    val a:Int = readLine()!!.toInt()\n    val b:Int = readLine()!!.toInt()\n    val n:Int = readLine()!!.toInt()\n    println("${a * n} ${b * n}")\n}'
    current_pair = tth.check_task('pies', kotlin_code, language=LANGUAGE.KOTLIN.value)
    return current_pair, (8, 3)


def get_kotlin_code_test_not_solved_solution():
    kotlin_code = 'fun main(args: Array<String>) {\n    val a:Int = readLine()!!.toInt()\n    val b:Int = readLine()!!.toInt()\n}'
    current_pair = tth.check_task('pies', kotlin_code, language=LANGUAGE.KOTLIN.value)
    return current_pair, (8, 0)


def get_kotlin_code_test_error_solution():
    kotlin_code = 'fun main(args: Arr<String>) {\n    val a:Int = readLine()!!.toInt()\n    val b:Int = readLine()!!.toInt()\n}'
    current_pair = tth.check_task('pies', kotlin_code, language=LANGUAGE.KOTLIN.value)
    return current_pair, (8, 0)


# Cpp tests
def get_cpp_code_test_data_full_solution():
    cpp_code = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int a;\n    std::cin >> a;\n    int b;\n    std::cin >> b;\n    int n;\n    std::cin >> n;\n    cout << a * n + b * n / 100 << " " << b * n % 100 << endl;\n    return 0;\n}'
    current_pair = tth.check_task('pies', cpp_code, language=LANGUAGE.CPP.value)
    return current_pair, (8, 8)


def get_cpp_code_test_data_partial_solution():
    cpp_code = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int a;\n    std::cin >> a;\n    int b;\n    std::cin >> b;\n    int n;\n    std::cin >> n;\n    cout << a * n << " " << b * n << endl;\n    return 0;\n}'
    current_pair = tth.check_task('pies', cpp_code, language=LANGUAGE.CPP.value)
    return current_pair, (8, 3)


def get_cpp_code_test_data_not_solved_solution():
    cpp_code = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int a;\n    std::cin >> a;\n    int b;\n    std::cin >> b;\n    int n;\n    return 0;\n}'
    current_pair = tth.check_task('pies', cpp_code, language=LANGUAGE.CPP.value)
    return current_pair, (8, 0)


def get_cpp_code_test_data_error_solution():
    cpp_code = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int a;\n    std::cin >> a\n    int b;\n    std::cin >> b;\n    int n;\n    return 0;\n}'
    current_pair = tth.check_task('pies', cpp_code, language=LANGUAGE.CPP.value)
    return current_pair, (8, 0)


class TestRunTestMethods(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=consts.LOGGER_FILE, level=logging.INFO)

    # Python tests
    def test_python_code_test_data_full_solution(self):
        logging.basicConfig(filename=consts.LOGGER_FILE, level=logging.INFO)
        res, right_res = get_python_code_test_data_full_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_python_code_test_data_partial_solution(self):
        res, right_res = get_python_code_test_data_partial_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_python_code_test_data_not_solved_solution(self):
        res, right_res = get_python_code_test_data_not_solved_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_python_code_test_data_error_solution(self):
        res, right_res = get_python_code_test_data_error_solution()
        self.assertTrue(is_equals(res, right_res))

    # Java tests
    def test_java_code_test_data_full_solution(self):
        res, right_res = get_java_code_test_data_full_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_java_code_test_data_partial_solution(self):
        res, right_res = get_java_code_test_data_partial_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_java_code_test_data_not_solved_solution(self):
        res, right_res = get_java_code_test_data_not_solved_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_java_code_test_data_error_solution(self):
        res, right_res = get_java_code_test_data_error_solution()
        self.assertTrue(is_equals(res, right_res))

    # Kotlin tests
    def test_kotlin_code_test_data_full_solution(self):
        res, right_res = get_kotlin_code_test_data_full_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_kotlin_code_test_data_partial_solution(self):
        res, right_res = get_kotlin_code_test_data_partial_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_kotlin_code_test_data_not_solved_solution(self):
        res, right_res = get_kotlin_code_test_not_solved_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_kotlin_code_test_data_error_solution(self):
        res, right_res = get_kotlin_code_test_error_solution()
        self.assertTrue(is_equals(res, right_res))

    # Cpp tests
    def test_cpp_code_test_data_full_solution(self):
        res, right_res = get_cpp_code_test_data_full_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_cpp_code_test_data_partial_solution(self):
        res, right_res = get_cpp_code_test_data_partial_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_cpp_code_test_data_not_solved_solution(self):
        res, right_res = get_cpp_code_test_data_not_solved_solution()
        self.assertTrue(is_equals(res, right_res))

    def test_cpp_code_test_data_error_solution(self):
        res, right_res = get_cpp_code_test_data_error_solution()
        self.assertTrue(is_equals(res, right_res))
