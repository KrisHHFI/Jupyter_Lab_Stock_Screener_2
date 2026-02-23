from utils.yfinance.call_tracker import state


def get_yfinance_call_count():
    """Return current tracked yfinance call count."""
    return state._yfinance_call_count
