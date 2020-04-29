# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.util.strings_util import convert_camel_case_to_snake_case


class PrettyString:

    def separator_str_for_pretty_string_method(self, suffix: str) -> str:
        separator = '_______________'
        class_name = convert_camel_case_to_snake_case(self.__class__.__name__).upper()
        return f'\n\n{separator}{class_name}_{suffix}{separator}\n\n'

    def get_pretty_string(self) -> str:
        return f'{self.separator_str_for_pretty_string_method("START")}' \
               f'{self.__str__()}' \
               f'{self.separator_str_for_pretty_string_method("END")}'
