from utils.yfinance.call_tracker import state


def set_yfinance_call_delay(seconds):
    """Set delay (seconds) before each yfinance call after the first call."""
    state._yfinance_call_delay_seconds = max(0.0, float(seconds))
