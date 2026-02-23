from utils.yfinance.call_tracker import state


def reset_yfinance_call_count():
    """Reset tracked yfinance call count and log for a fresh run."""
    state._yfinance_call_count = 0
    state._yfinance_call_log = []
