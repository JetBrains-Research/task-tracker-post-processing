# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from statistics import median
from collections import Counter
from typing import List, Any, Optional, Union


def calculate_safety_median(values: List[int],
                            default_value: Optional[int] = None) -> Optional[Union[int, int]]:
    if len(values) == 0:
        return default_value
    return median(values)


# Todo: how can we do it better?
def calculate_median_for_objects(values: List[Any],
                                 default_value: Optional[Any] = None) -> Optional[Union[Any, Any]]:
    if len(values) == 0:
        return default_value
    values_and_freq = Counter(values)
    freq_median = median(values_and_freq.values())
    candidates = []
    for exp, freq in values_and_freq.items():
        if freq == freq_median:
            candidates.append(exp)
    candidates.sort()
    return candidates[0]
