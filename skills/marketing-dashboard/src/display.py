from __future__ import annotations

from typing import Iterable, Sequence

from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text


console = Console()


def print_heading(title: str) -> None:
    panel = Table.grid()
    panel.add_column()
    panel.add_row(Text(title, style="bold white"))
    console.print(panel)


def print_section(title: str) -> None:
    console.print(f"\n== {title} ==")


def print_kv_table(title: str, rows: Sequence[tuple[str, str]]) -> None:
    table = Table(title=title, box=box.ASCII, show_header=False)
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", justify="right", style="bold white")
    for key, value in rows:
        table.add_row(key, value)
    console.print(table)


def print_table(title: str, columns: Sequence[str], rows: Iterable[Sequence[str]]) -> None:
    table = Table(title=title, box=box.ASCII, show_header=True, header_style="bold cyan")
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def print_warning(message: str) -> None:
    console.print(f"[yellow]warn:[/yellow] {message}")


def print_error(message: str) -> None:
    console.print(f"[red]error:[/red] {message}")


def sparkline(values: Sequence[float]) -> str:
    if not values:
        return ""
    ticks = " .:-=+*#%@"
    low = min(values)
    high = max(values)
    if high == low:
        return ticks[-1] * len(values)
    scale = (len(ticks) - 1) / (high - low)
    out = []
    for val in values:
        idx = int((val - low) * scale)
        out.append(ticks[idx])
    return "".join(out)
