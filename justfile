set export := true
set dotenv-load := true

VENV_DIRNAME := ".venv"

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
    if test ! -e $VENV_DIRNAME; then \
        uv python install; \
    fi
    just update

# Install and/or update all dependencies defined in pyproject.toml
@update: check_uv
    uv sync --all-extras --upgrade

# Format
@format: bootstrap
    ruff format .
    ruff check . --fix

