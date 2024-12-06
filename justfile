set export := true
set dotenv-load := true

VENV_DIRNAME := ".venv"
VERSION := `sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`

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
    if test ! -e {{VENV_DIRNAME}}; then \
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

# Build
@build: bootstrap
	uv build
	uvx twine check dist/*
	uvx check-manifest
	uvx pyroma .
	uvx check-wheel-contents dist

# Clean
@clean:
	rm -rf build dist src/*.egg-info .coverage*

# Check if the current Git branch is 'main'
@branch:
    if [ "`git rev-parse --abbrev-ref HEAD`" = "main" ]; then \
        echo "On branch main."; \
    else \
        echo "Error - Not on branch main."; \
        exit 1; \
    fi

# Check if the working directory is clean
@porcelain:
    if [ -z "`git status --porcelain`" ]; then \
        echo "Working directory is clean."; \
    else \
        echo "Error - working directory is dirty. Commit your changes."; \
        exit 1; \
    fi

# Version number
@version:
    echo "{{VERSION}}"
