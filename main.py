from typing import Annotated, Final

import httpx
from rich.console import Console
from typer import Argument, Typer

from utils import check_website, display_website_stats, normalize_url

app = Typer()
console = Console()
err_console = Console(stderr=True)

TIMEOUT: Final[int] = 10


@app.command(help="Check the status of websites.")
def website_status(
    url: Annotated[
        str, Argument(help="The url of which you want to check the status of")
    ] = "https://indently.io/",
) -> None:
    url = normalize_url(url)

    try:
        stats = check_website(url, TIMEOUT)

        display_website_stats(url, stats, console)
    except httpx.HTTPError as exc:
        err_console.print(f"An error occurred for {exc.request.url}!")
        err_console.print("Please check the url and try again!")


if __name__ == "__main__":
    app()
