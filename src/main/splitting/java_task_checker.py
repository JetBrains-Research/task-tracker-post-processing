import os
import logging

import javalang
from javalang.tokenizer import LexerError
from javalang.parser import JavaSyntaxError, JavaParserError

from src.main.util import consts
from src.main.util.consts import LANGUAGE
from src.main.util.language_util import get_extension_by_language
from src.main.util.file_util import create_file, get_name_from_path
from src.main.splitting.task_checker import ITaskChecker, check_call_safely, check_output_safely, SOURCE_OBJECT_NAME, \
    TASKS_TESTS_PATH, SOURCE_FOLDER


log = logging.getLogger(consts.LOGGER_NAME)


class JavaTaskChecker(ITaskChecker):
    def __init__(self):
        self.package = ''

    @property
    def language(self):
        return LANGUAGE.JAVA.value

    # class A{
    # public static void main(String args[]){
    # Scanner in=new Scanner(System.in);
    # Int a=in.nextInt();
    # System.out.print(a);}}
    @property
    def min_symbols_number(self):
        return 140

    @property
    def output_strings(self):
        return ['System.out.print']

    # https://github.com/c2nes/javalang
    def get_java_class_name(self, source_code: str):
        try:
            tree = javalang.parse.parse(source_code)
            name = next(clazz.name for clazz in tree.types
                        if isinstance(clazz, javalang.tree.ClassDeclaration)
                        for m in clazz.methods
                        if m.name == 'main' and m.modifiers.issuperset({'public', 'static'}))
            if tree.package:
                log.info(f'Java source code package is {tree.package.name}')
                self.package = tree.package.name + '.'
            return name
        except (JavaSyntaxError, JavaParserError, LexerError) as e:
            log.info('Java lexer/parser exception was raised')
            log.exception(e)
            return SOURCE_OBJECT_NAME
        except Exception as e:
            log.exception(e)
            return SOURCE_OBJECT_NAME

    def create_source_file(self, source_code: str):
        source_file_name = self.get_java_class_name(source_code)
        source_code_file = os.path.join(TASKS_TESTS_PATH, SOURCE_OBJECT_NAME,
                                        source_file_name + get_extension_by_language(self.language))
        create_file(source_code, source_code_file)
        return source_code_file

    def is_source_file_correct(self, source_file: str):
        args = ['javac', source_file, '-d', SOURCE_FOLDER]
        is_correct = check_call_safely(args, None)
        log.info(f'Source code is correct: {is_correct}')
        return is_correct

    def run_test(self, input: str, expected_output: str, source_file: str):
        args = ['java', '-cp', SOURCE_FOLDER, self.package + get_name_from_path(source_file, False)]
        return check_output_safely(input, expected_output, args)
