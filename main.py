from typing import Annotated

import httpx
from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

app = Typer()

console = Console()
err_console = Console(stderr=True)


@app.command()
def website_status(
    url: Annotated[
        str, Argument(help="The url of which you want to check the status of")
    ] = "https://www.indently.io",
):
    """
    Check the status of URL.
    """
    try:
        r = httpx.get(url)

        table = Table(show_header=False, show_lines=True)
        table.add_row("URL", url)
        table.add_row("Status Code", str(r.status_code))
        table.add_row("Content Type", r.headers["Content-Type"])
        table.add_row("Server", r.headers["Server"])
        table.add_row("Response time", f"{r.elapsed.total_seconds()}s")
        console.print(table)
    except httpx.HTTPError as exc:
        err_console.print("An Error Occurred, please try again!")
        err_console.print(str(exc))


if __name__ == "__main__":
    app()
