from time import sleep

from utils.yfinance.call_tracker import state
from utils.yfinance.call_tracker.increment_yfinance_call_count import increment_yfinance_call_count
from utils.yfinance.call_tracker.timestamp_now import timestamp_now


def log_yfinance_call(action):
    """Track and delay yfinance calls; messages are shown by metadata printer."""
    if state._yfinance_call_count > 0 and state._yfinance_call_delay_seconds > 0:
        sleep(state._yfinance_call_delay_seconds)

    call_number = increment_yfinance_call_count()
    timestamp = timestamp_now()
    message = f"Call #{call_number} at {timestamp} -> {action}"
    state._yfinance_call_log.append(message)
