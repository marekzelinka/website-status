from dataclasses import dataclass

import httpx
from rich.console import Console
from rich.table import Table


def normalize_url(url: str) -> str:
    """Formats url by adding http(s):// if it is missing."""
    return url if url.startswith(("http://", "https://")) else f"https://{url}"


@dataclass
class WebsiteStats:
    status_code: int
    status_phrase: str
    content_type: str
    encoding: str
    server: str
    response_time: float


def check_website(url: str, timeout: float) -> WebsiteStats:
    """Retuns response stats for provided url."""
    response = httpx.get(url, follow_redirects=True, timeout=timeout)
    response.raise_for_status()

    status_code = response.status_code
    status_phrase = response.reason_phrase
    content_type = response.headers.get("Content-Type", "Unknown")
    encoding = response.encoding or "Unknown"
    server = response.headers.get("Server", "Unknown")
    response_time = response.elapsed.total_seconds()

    return WebsiteStats(
        status_code=status_code,
        status_phrase=status_phrase,
        content_type=content_type,
        encoding=encoding,
        server=server,
        response_time=response_time,
    )


def display_website_stats(url: str, stats: WebsiteStats, console: Console) -> None:
    """Prints website stats in a formatted table."""
    table = Table("Param", "Value", show_lines=True)

    table.add_row("URL", url)
    table.add_row("Status Code", f"{stats.status_code} ({stats.status_phrase})")
    table.add_row("Content Type", stats.content_type)
    table.add_row("Encoding", stats.encoding)
    table.add_row("Server", stats.server)
    table.add_row("Response time", f"{stats.response_time:.2f}s")

    console.print(table)
