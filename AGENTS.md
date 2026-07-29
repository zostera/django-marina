# django-marina — Agent Guide

Django extensions by [Zostera](https://github.com/zostera). Provides database utilities,
HTML helpers, and test infrastructure shared across Zostera's Django packages.

## Related packages

These packages share tooling and conventions — changes in one often mirror to others:

- `https://github.com/zostera/django-bootstrap3` — Bootstrap 3 for Django
- `https://github.com/zostera/django-bootstrap4` — Bootstrap 4 for Django
- `https://github.com/zostera/django-bootstrap5` — Bootstrap 5 for Django
- `https://github.com/zostera/django-icons` — Icons for Django
- `https://github.com/zostera/django-marina` — Django extensions by Zostera (this package)

Config files (justfile, tox.ini, pyproject.toml, etc.) are kept in sync across packages.
AGENTS.md is **not** synced — each package has its own.

## Setup

Requires [uv](https://github.com/astral-sh/uv) and [just](https://github.com/casey/just).

```
just install    # install deps from uv.lock
just upgrade    # upgrade all deps
```

Never invoke `python`, `pip`, or `ruff` directly. All commands go through `just`, which delegates to `uv run` (venv) or `uvx` (ephemeral tools like ruff, twine, check-manifest).

`uv.lock` is fully generated — never manually resolve merge conflicts in it. On conflict: accept either side, then run `just upgrade` to regenerate.

Also run `just upgrade` after changing any dependency constraint in `pyproject.toml` (e.g. bumping the Django floor) — otherwise `uv.lock`'s own `requires-dist` metadata goes stale and silently drifts from `pyproject.toml`.

## Key commands

```
just test           # run tests (single Python/Django version)
just test-cov       # run tests with coverage report
just tests          # run full tox matrix (all Python × Django combos)
just lint           # check formatting and style (ruff)
just format         # auto-fix formatting and style
just build          # build + packaging checks (preflight before release)
just docs           # build Sphinx documentation
just example        # run the example Django project
just version        # print current package version
```

## Code style

- **Formatter/linter**: ruff (line length 120)
- **Docstrings**: pydocstyle D2xx/D4xx rules; D1xx (missing docstring) is ignored
- `ruff check --fix` auto-fixes isort, pyupgrade, and some flake8 issues
- `F8` (unused names) is not auto-fixed — fix manually

Run `just lint` before committing. CI enforces it.

## Package structure

```
src/django_marina/
    __about__.py        version string
    __init__.py         exports __version__
    db/
        migrations.py   migration helpers
        models.py       abstract model mixins
    html.py             HTML utility functions (uses beautifulsoup4)
    test/
        clients.py      test client helpers
        runners.py      test runner helpers
        test_cases.py   base TestCase classes
```

## Testing

**Test runner is Django's test runner, not pytest.** Use `manage.py test` or `just test`.

```
tests/
    app/                minimal Django project used as test harness
        settings.py
        urls.py
        views.py
    smoke_test.py       import smoke test (run against built wheel/tarball)
    test_db.py
    test_extended_client.py
    test_extended_test_case.py
    test_html.py
    test_imports.py
    test_temp_media_runner.py
    test_version.py
```

The current Python × Django matrix is not a full grid — see `tox.ini`'s `envlist` for what's actually tested (`pyproject.toml` classifiers and `ci.yml`'s matrix must match it). Don't copy the matrix into prose elsewhere; it drifts. See [MAINTAINING.md](MAINTAINING.md) for the policy behind how the matrix is chosen and kept current.

Target the matrix when adding features; avoid Django-version-specific code paths where possible.

## CI

GitHub Actions runs on every push and PR:
- `ci.yml` — lint + full tox matrix
- `release.yml` — publishes to PyPI on version tags

`just lint` must pass before committing — CI enforces it and will fail the PR.

See [MAINTAINING.md](MAINTAINING.md) for the release process and version-support policy.
