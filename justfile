# use with https://github.com/casey/just

# default recipe
default:
  just --list

[private]
@check_uv:
    if ! command -v uv &> /dev/null; then \
        echo "uv could not be found. Exiting."; \
        exit 1; \
    fi

# Set up development environment
@bootstrap: check_uv
    if test ! -e .venv; then \
        uv python install; \
    fi
    uv sync

# Format
@format: bootstrap
	ruff format .
	ruff check . --fix
