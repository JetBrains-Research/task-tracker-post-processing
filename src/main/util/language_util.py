# Copyright (c) by anonymous author(s)

from src.main.util import consts


def get_language_by_extension(extension: consts.EXTENSION) -> consts.LANGUAGE:
    return consts.EXTENSION_TO_LANGUAGE_DICT.get(extension, consts.LANGUAGE.UNDEFINED)


def get_extension_by_language(language: consts.LANGUAGE) -> consts.EXTENSION:
    for extension, cur_language in consts.EXTENSION_TO_LANGUAGE_DICT.items():
        if cur_language == language:
            return extension
    return consts.EXTENSION.EMPTY
