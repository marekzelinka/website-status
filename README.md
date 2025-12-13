# Website Status

Simple utility cli-based app that helps users check the status of any website url.

## Usage

This project uses the modern `pyproject.toml` standard for dependency management and requires the `uv` tool to manage the environment.

```sh
uv run main.py [URL]
```

For example:

```sh
uv run main.py https://github.com/marekzelinka/website-checker
```

## Technologies Used

- **Python** - duh
- **Typer** - cli ui
- **httpx** - http client for Python3
