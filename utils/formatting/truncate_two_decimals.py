import math


def truncate_two_decimals(value):
    """Truncate a number to 2 decimal places without rounding."""
    try:
        numeric_value = float(value)
        if not math.isfinite(numeric_value):
            return "N/A"
        return math.trunc(numeric_value * 100) / 100
    except (TypeError, ValueError, OverflowError):
        return value
