# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.util import consts


def get_language_by_extension(extension: str):
    return consts.EXTENSION_TO_LANGUAGE_DICT.get(extension, consts.LANGUAGE.NOT_DEFINED.value)


def get_extension_by_language(language: consts.LANGUAGE):
    for extension, cur_language in consts.EXTENSION_TO_LANGUAGE_DICT.items():
        if cur_language == language:
            return extension
    return None
