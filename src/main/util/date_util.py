import re
from datetime import datetime

from src.main.util import consts


# Delete : symbol from hours in timestamp for the correct conversion to datetime
# For example 2019-12-09T18:41:28.548+03:00 -> 2019-12-09T18:41:28.548+0300
def corrected_time(timestamp: str):
    return re.sub(r'([-+]\d{2}):(\d{2})$', r'\1\2', timestamp)


def get_datetime_by_format(date, datetime_format=consts.DATE_TIME_FORMAT):
    return datetime.strptime(corrected_time(date), datetime_format)
