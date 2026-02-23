from utils.yfinance.call_tracker import state


def get_yfinance_call_log():
    """Return the tracked yfinance call log entries."""
    return list(state._yfinance_call_log)
