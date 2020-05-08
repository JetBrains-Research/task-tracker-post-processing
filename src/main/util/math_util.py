# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Optional, Any, List
from statistics import median, StatisticsError

from src.main.util.consts import LOGGER_NAME

log = logging.getLogger(LOGGER_NAME)


def get_safety_median(values: List[Any], default_value: Optional[Any] = None) -> Optional[Any]:
    try:
        return median(values)
    except StatisticsError:
        log.info(f'Have gotten empty list to calculate median. Return default value:{default_value}')
        return default_value
