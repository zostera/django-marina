# django-marina: Agent Guide

Django extensions by [Zostera](https://github.com/zostera). Provides database utilities,
HTML helpers, and test infrastructure shared across Zostera's Django packages.

## Related packages

These packages share tooling and conventions. Changes in one often mirror to others:

- `https://github.com/zostera/django-bootstrap3`, Bootstrap 3 for Django
- `https://github.com/zostera/django-bootstrap4`, Bootstrap 4 for Django
- `https://github.com/zostera/django-bootstrap5`, Bootstrap 5 for Django
- `https://github.com/zostera/django-icons`, Icons for Django
- `https://github.com/zostera/django-marina`, Django extensions by Zostera (this package)

Config files (justfile, tox.ini, pyproject.toml, etc.) are kept in sync across packages.
AGENTS.md is **not** synced, each package has its own.

## Setup

Requires [uv](https://github.com/astral-sh/uv) and [just](https://github.com/casey/just). Run `just` for the command list.

Never invoke `python`, `pip`, or `ruff` directly. All commands go through `just`, which delegates to `uv run` (venv) or `uvx` (ephemeral tools like ruff, twine, check-manifest).

`uv.lock` is fully generated, never manually resolve merge conflicts in it. On conflict: accept either side, then run `just upgrade` to regenerate.

Also run `just upgrade` after changing any dependency constraint in `pyproject.toml` (e.g. bumping the Django floor). Otherwise `uv.lock`'s own `requires-dist` metadata goes stale and silently drifts from `pyproject.toml`.

## Code style

ruff, configured in `[tool.ruff]` in `pyproject.toml`. `just format` fixes, `just lint` checks. Run it before committing, CI enforces it.

## Testing

**Test runner is Django's test runner, not pytest.** Use `manage.py test` or `just test`.

The current Python × Django matrix is not a full grid. See `tox.ini`'s `envlist` for what's actually tested (`pyproject.toml` classifiers and `ci.yml`'s matrix must match it). Don't copy the matrix into prose elsewhere; it drifts. See [MAINTAINING.md](MAINTAINING.md) for the policy behind how the matrix is chosen and kept current.

Target the matrix when adding features; avoid Django-version-specific code paths where possible.

## CI

`just lint` must pass before committing, CI enforces it and will fail the PR.

See [MAINTAINING.md](MAINTAINING.md) for the release process and version-support policy.
