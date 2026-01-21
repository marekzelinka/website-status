import asyncio
from functools import wraps
from typing import Annotated

import httpx
from rich.console import Console
from typer import Argument, Typer

from utils import display_website_stats, get_website_status

app = Typer()
console = Console()
err_console = Console(stderr=True)


@app.command(help="Check the status of a website url.")
@lambda f: wraps(f)(
    lambda *a, **kw: asyncio.run(f(*a, **kw))
)  # Workaround for Typer async support
async def check_website(url: Annotated[str, Argument()]) -> None:
    console.print(f"Checking {url}...")

    try:
        stats = await get_website_status(url)
        display_website_stats(stats, console)
    except httpx.HTTPError as exc:
        err_console.print(
            f"An error occurred for {exc.request.url} - check and try again..."
        )


@app.command(help="Check the statuses of a list of website urls.")
@lambda f: wraps(f)(
    lambda *a, **kw: asyncio.run(f(*a, **kw))
)  # Workaround for Typer async support
async def check_websites(
    urls: Annotated[list[str], Argument(help="The list of urls to check.")],
) -> None:
    print(f"Checking {len(urls)} {'websites' if len(urls) > 1 else 'website'}...")

    tasks = [get_website_status(url) for url in urls]

    try:
        for completed_task in asyncio.as_completed(tasks, timeout=10):
            try:
                stats = await completed_task
                display_website_stats(stats, console)
            except httpx.HTTPError as exc:
                err_console.print(
                    f"An error occurred for {exc.request.url} - check and try again..."
                )
    except TimeoutError:
        err_console.print("Timeout reached — some websites took too long.")


if __name__ == "__main__":
    app()
