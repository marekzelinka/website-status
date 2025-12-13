start *ARGS:
    uv run main.py {{ARGS}}

typecheck:
    uv run ty check

lint:
    uv run ruff check --fix
