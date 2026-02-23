from utils.formatting.truncate_two_decimals import truncate_two_decimals


def format_compact_number(value):
    """Convert large numeric values into compact human-readable format (M/B/T)."""
    try:
        numeric_value = float(value)
        thresholds = [
            (1_000_000_000_000, "T"),
            (1_000_000_000, "B"),
            (1_000_000, "M"),
        ]

        for threshold, suffix in thresholds:
            if numeric_value >= threshold:
                return f"{truncate_two_decimals(numeric_value / threshold)}{suffix}"

        return str(numeric_value)
    except (TypeError, ValueError):
        return value