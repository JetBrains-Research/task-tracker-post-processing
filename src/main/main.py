# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import sys
import logging

sys.path.append('.')
sys.path.append('../..')
from src.main.util import consts
from src.main.util.log_util import configure_logger

log = logging.getLogger(consts.LOGGER_NAME)


def main() -> None:
    configure_logger(to_delete_previous_logs=True)


if __name__ == '__main__':
    main()
