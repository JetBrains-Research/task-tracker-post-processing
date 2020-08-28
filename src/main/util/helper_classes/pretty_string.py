# Copyright (c) by anonymous author(s)

from src.main.util.strings_util import convert_camel_case_to_snake_case


class PrettyString:
    _separator = '_______________'

    def get_class_separator(self, suffix: str) -> str:
        class_name = convert_camel_case_to_snake_case(self.__class__.__name__).upper()
        return f'\n\n{self._separator}{class_name}_{suffix}{self._separator}\n\n'

    def get_pretty_string(self) -> str:
        return f'{self.get_class_separator("START")}' \
               f'{self.__str__()}' \
               f'{self.get_class_separator("END")}'
