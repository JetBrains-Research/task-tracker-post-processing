import logging
import unittest

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.test.tasks_tests_handler.util import test_task, SOLUTION

python_test_data = {
    SOLUTION.FULL.value :
        ['a = int(input())\nb = int(input())\nn = int(input())\nprint(str((a * 100 * n + b * n) // 100) + " '
         '" + str((a * 100 * n + b * n) % 100)) ',
         (8, 8)],
    SOLUTION.PARTIAL.value :
        ['a = int(input())\nb = int(input())\nn = int(input())\nprint(str(a * n) + " " + str((b * n)))',
         (8, 3)],
    SOLUTION.WRONG.value :
        ['a = int(input())\n',
         (8, 0)],
    SOLUTION.ERROR.value :
        ['a = int(input())\nb = int(input()\nn = int(input())\nprint(str(a * n) + " " + str((b * n)))',
         (8, 0)]
}

java_test_data = {
    SOLUTION.FULL.value :
        ['import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader(System.in);\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n        System.out.println((a * n + b * n / 100) + " " + (b * n % 100));\n    }\n}',
         (8, 8)],
    SOLUTION.PARTIAL.value :
        ['import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader(System.in);\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n        System.out.println(a * n + " " + b * n);\n    }\n}',
         (8, 3)],
    SOLUTION.WRONG.value :
        ['import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader(System.in);\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n    }\n}',
         (8, 0)],
    SOLUTION.ERROR.value :
        ['import java.io.*;\nclass test { \n\n    public static void main(String args[])throws IOException\n    {\n        InputStreamReader in=new InputStreamReader();\n        BufferedReader br=new BufferedReader(in);\n       int a=Integer.parseInt(br.readLine());\n        int b=Integer.parseInt(br.readLine());\n       int n=Integer.parseInt(br.readLine());\n        System.out.println(a * n + " " + b * n);\n    }\n}',
         (8, 0)]
}

kotlin_test_data = {
    SOLUTION.FULL.value :
        ['fun main(args: Array<String>) {\n    val a:Int = readLine()!!.toInt()\n    val b:Int = readLine()!!.toInt()\n    val n:Int = readLine()!!.toInt()\n    println("${a * n + b * n / 100} ${b * n % 100}")\n}',
         (8, 8)],
    SOLUTION.PARTIAL.value :
        ['fun main(args: Array<String>) {\n    val a:Int = readLine()!!.toInt()\n    val b:Int = readLine()!!.toInt()\n    val n:Int = readLine()!!.toInt()\n    println("${a * n} ${b * n}")\n}',
         (8, 3)],
    SOLUTION.WRONG.value :
        ['fun main(args: Array<String>) {\n    val a:Int = readLine()!!.toInt()\n    val b:Int = readLine()!!.toInt()\n}',
         (8, 0)],
    SOLUTION.ERROR.value :
        ['fun main(args: Arr<String>) {\n    val a:Int = readLine()!!.toInt()\n    val b:Int = readLine()!!.toInt()\n}',
         (8, 0)]
}

cpp_test_data = {
    SOLUTION.FULL.value :
        ['#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int a;\n    std::cin >> a;\n    int b;\n    std::cin >> b;\n    int n;\n    std::cin >> n;\n    cout << a * n + b * n / 100 << " " << b * n % 100 << endl;\n    return 0;\n}',
         (8, 8)],
    SOLUTION.PARTIAL.value :
        ['#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int a;\n    std::cin >> a;\n    int b;\n    std::cin >> b;\n    int n;\n    std::cin >> n;\n    cout << a * n << " " << b * n << endl;\n    return 0;\n}',
         (8, 3)],
    SOLUTION.WRONG.value :
        ['#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int a;\n    std::cin >> a;\n    int b;\n    std::cin >> b;\n    int n;\n    return 0;\n}',
         (8, 0)],
    SOLUTION.ERROR.value :
        ['#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int a;\n    std::cin >> a\n    int b;\n    std::cin >> b;\n    int n;\n    return 0;\n}',
         (8, 0)]
}


class TestPiesTests(unittest.TestCase):
    task = 'pies'

    def setUp(self) -> None:
        logging.basicConfig(filename=consts.LOGGER_TEST_FILE, level=logging.INFO)

    def test_python(self):
        test_task(self, python_test_data, LANGUAGE.PYTHON.value)

    def test_java(self):
        test_task(self, java_test_data, LANGUAGE.JAVA.value)

    def test_kotlin(self):
        test_task(self, kotlin_test_data, LANGUAGE.KOTLIN.value)

    def test_cpp(self):
        test_task(self, cpp_test_data, LANGUAGE.CPP.value)
