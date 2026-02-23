from datetime import datetime

import pandas as pd
from rich.console import Console

from utils.formatting.format_timestamp import format_timestamp
from utils.printing.display_styled_table import display_styled_table
from utils.printing.print_header import print_header

_console = Console()


def print_data_collected(
    collected_at=None,
    yfinance_call_count=None,
    yfinance_call_delay=None,
    yfinance_call_log=None,
):
    """Print usage + data collection table two lines below prior output."""
    timestamp = collected_at or datetime.now()
    call_count = yfinance_call_count if yfinance_call_count is not None else "N/A"
    call_delay = yfinance_call_delay if yfinance_call_delay is not None else "N/A"

    print("\n\n", end="")
    print_header("Call metadata")

    usage_table = pd.DataFrame(
        [
            ["yfinance calls made", call_count],
            ["Call delay (seconds)", call_delay],
            ["Data collected on", format_timestamp(timestamp)],
        ],
        columns=["Metric", "Value"],
    )
    display_styled_table(usage_table)

    if yfinance_call_log:
        _console.print("\n[bold black]CALL LOG[/bold black]")
        display_styled_table(pd.DataFrame([[entry] for entry in yfinance_call_log], columns=["Entry"]))
