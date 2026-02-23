from datetime import datetime

from utils.formatting.format_timestamp import format_timestamp


def timestamp_now():
    return format_timestamp(datetime.now())
