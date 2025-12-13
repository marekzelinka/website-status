from typing import Annotated

from typer import Argument, Typer

app = Typer()


@app.command()
def website_status(
    url: Annotated[
        str, Argument(help="The url of which you want to check the status of")
    ] = "https://www.indently.io",
):
    """
    Check the status of URL.
    """
    print(url)


if __name__ == "__main__":
    app()
