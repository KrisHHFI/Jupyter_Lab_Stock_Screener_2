from utils.yfinance.call_tracker import state


def increment_yfinance_call_count():
    """Increment and return the tracked yfinance call count."""
    state._yfinance_call_count += 1
    return state._yfinance_call_count
