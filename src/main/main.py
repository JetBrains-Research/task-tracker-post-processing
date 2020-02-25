# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

from src.main.util.consts import LOGGER_FILE, LOGGER_NAME, LOGGER_FORMAT

log = logging.getLogger(LOGGER_NAME)


def main():
    logging.basicConfig(filename=LOGGER_FILE, format=LOGGER_FORMAT, level=logging.INFO)
    pass


if __name__ == '__main__':
    main()
