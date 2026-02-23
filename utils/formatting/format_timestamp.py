from datetime import datetime


def format_timestamp(value, pattern="%Y-%m-%d %H:%M:%S"):
    """Format datetime-like values to a consistent timestamp string."""
    if isinstance(value, datetime):
        return value.strftime(pattern)

    if isinstance(value, bool):
        return str(value)

    if isinstance(value, (int, float)):
        try:
            timestamp = float(value)
            if timestamp <= 0:
                return value
            if timestamp >= 1_000_000_000_000:
                timestamp = timestamp / 1000.0
            return datetime.fromtimestamp(timestamp).strftime(pattern)
        except (OSError, OverflowError, ValueError):
            return value

    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value)
            return parsed.strftime(pattern)
        except ValueError:
            return value

    return str(value)