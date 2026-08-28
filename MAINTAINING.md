# Maintaining django-marina

Notes for maintainers. For how to submit a contribution, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Version support policy

These are rules, not a snapshot of current versions — the current matrix lives in `tox.ini`
(`envlist`), `.github/workflows/ci.yml` (the `python_django_matrix` job), and `pyproject.toml`
(classifiers + `dependencies`). Those three files are the source of truth and must agree with
each other. Don't restate the matrix as a table in prose docs (AGENTS.md, README, etc.) — a
copy always drifts out of sync with the files that actually enforce it.

- Support every Python and Django release cycle that is not end-of-life, per
  [endoflife.date/python](https://endoflife.date/python) and
  [endoflife.date/django](https://endoflife.date/django). Drop a cycle from the matrix as soon
  as it goes EOL — don't wait for a scheduled release to do it.
- Always track Django's `main` branch in the matrix. Add a new Django release series
  (e.g. 6.1) alongside `main` as soon as `main` has diverged from it — i.e. once upstream
  cuts a `stable/X.Y.x` branch and `main` itself moves on to the next alpha. Don't wait for
  the new series' final release.
- Add a new Python pre-release as a **non-blocking** CI job (`continue-on-error: true`) as
  soon as it's installable — `uv python install` can usually fetch a new CPython the same day
  it's cut, so the interpreter itself is rarely the blocker. Only make the job blocking once
  test dependencies with C extensions publish wheels for it, if any are in use.

## Maintenance round

Start every maintenance round — and every release — by reconciling the support matrix with
reality, not from memory:

1. Check [endoflife.date/python](https://endoflife.date/python) and
   [endoflife.date/django](https://endoflife.date/django) for what is currently supported.
   The JSON endpoints (`https://endoflife.date/api/python.json`, `.../django.json`) are easier
   to diff against the matrix than the pages.
2. Drop every cycle that has gone EOL, and add every new one, per the policy above.
3. Reconcile all three sources of truth together — `tox.ini` (`envlist`),
   `.github/workflows/ci.yml` (`python_django_matrix`), and `pyproject.toml` (classifiers and
   the `Django` dependency). They drift independently, so check all three even when only one
   looks wrong.
4. Record any change as a `CHANGELOG.md` entry — dropping a cycle raises the dependency floor
   and is a breaking change for anyone on it. Under the `YY.N` version scheme the number
   carries no such signal, so the note is the only warning those users get.

## Release process

1. On a release branch, update `CHANGELOG.md` and bump `version` in `pyproject.toml`; open a PR and merge it
2. Check out and pull `main`
3. `just build` — builds wheel + tarball, runs packaging checks, and smoke-tests both against an isolated env
4. `just release-tag` — creates and pushes the version tag; GitHub Actions publishes to PyPI

`main` is protected — direct pushes are rejected (or bypass branch protection, which is worse). Always land the
version bump through a PR like any other change.

`just release-tag` requires a clean working directory and the current branch to be `main`. It will fail otherwise.

Order the release notes so the support-matrix changes lead: dropped Python/Django first, then
added Python/Django, then everything else. Those are the entries a user upgrading needs to see,
and they are easy to lose in a long list.
