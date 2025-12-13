from typing import Annotated

import httpx
from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

app = Typer()
console = Console()


@app.command()
def website_status(
    url: Annotated[
        str, Argument(help="The url of which you want to check the status of")
    ] = "https://www.indently.io",
):
    """
    Check the status of URL.
    """
    r = httpx.get(url)

    table = Table(show_header=False, show_lines=True)
    table.add_row("URL", url)
    table.add_row("Status Code", str(r.status_code))
    table.add_row("Content Type", r.headers["Content-Type"])
    table.add_row("Server", r.headers["Server"])
    table.add_row("Response time", f"{r.elapsed.total_seconds()}s")
    console.print(table)


if __name__ == "__main__":
    app()
