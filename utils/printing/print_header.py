from rich.console import Console
from rich.rule import Rule

_console = Console()


def print_header(title, main_header=False):
    """Print a section header; optionally use main header style."""
    text = title.upper()

    if main_header:
        _console.print(Rule(title=f"[bold black]{text}[/bold black]", style="grey50"))
        return

    _console.print(Rule(title=f"[bold black]{text}[/bold black]", style="grey50"))
