from typing import Annotated

import httpx
from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

app = Typer()
console = Console()
err_console = Console(stderr=True)


@app.command(help="Check the status of websites.")
def website_status(
    url: Annotated[
        str, Argument(help="The url of which you want to check the status of")
    ] = "https://indently.io/",
) -> None:
    try:
        r = httpx.get(url, follow_redirects=True)
        r.raise_for_status()

        status_code = str(r.status_code)
        content_type = r.headers.get("Content-Type", "Unknown")
        server = r.headers.get("Server", "Unknown")
        response_time = r.elapsed.total_seconds()

        table = Table("Param", "Value", show_lines=True)
        table.add_row("URL", url)
        table.add_row("Status Code", status_code)
        table.add_row("Content Type", content_type)
        table.add_row("Server", server)
        table.add_row("Response time", f"{response_time:.2f}s")
        console.print(table)
    except httpx.HTTPError as exc:
        err_console.print("An Error Occurred, please try again!")
        err_console.print(str(exc))


if __name__ == "__main__":
    app()
