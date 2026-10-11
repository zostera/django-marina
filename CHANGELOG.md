# Changelog

## Unreleased

- Add `.gitattributes` with `* text=auto`, so the repository stores text files with LF whatever the committing machine used. `.editorconfig` asked for this and could not enforce it.
- Drop `max_line_length` for Python from `.editorconfig`. It said 88 while ruff enforces 120, so an editor honouring it flagged code that passes lint.

## Unreleased

- List `.github/dependabot.yml` in PACKAGING.md as synced identically. All five packages already carried the same file; nothing said so.

## Unreleased

- Say in MAINTAINING.md that `just release-check` reporting no `Unreleased` entries straight after a cut means nothing is pending, not that the changelog was lost.
- Say in PACKAGING.md that git files a propagation's changelog entry under a freshly dated heading silently, so the fresh-`Unreleased` rule only helps if it is remembered.

## Unreleased

- Fix the numbering of the release-note ordering list in MAINTAINING.md, broken while renumbering the release process in the previous change.
- Show commits that touch nothing in `src/` in `just release-check` as a second group, instead of hiding them. Tooling, CI and documentation changes belong in the release notes too, and the old output read as a complete list while being a filtered one.
- Fail `just build` when `uv.lock` does not name the version in `pyproject.toml`, and add `just relock` to fix it. `uv sync --frozen` does not check the project's own version, so a stale lock passed every packaging check.
- Say in PACKAGING.md that a propagation branch starts from `main`, never from an open release branch, which is how two siblings cut a version that was never published.

## 26.3 (2026-10-11)

- **Breaking:** Drop support for Python 3.10, end of life since 2026-10-01. The floor is now Python 3.11.
- Test on Python 3.15 against Django 6.1 and `main`. The job is non-blocking and 3.15 is
  not advertised as supported, because no Django release claims it yet.
- Remove the `<7.0` upper bound on the `Django` dependency.
- Hold coverage at 100%. `fail_under = 100` fails the build, in CI and locally, on a drop.
- Harden the workflows after a `zizmor` audit: the Dependabot job decides from the pull request author rather than `github.actor`, which a `pull_request_target` workflow cannot trust; `ci.yml` runs with `contents: read` instead of the repository default; and the job that publishes to PyPI no longer restores a shared cache. MAINTAINING.md gains a dependency update policy saying what auto-merges and what waits for a person.
- Fail the CI gate when any job fails, not only the test matrix. A failing docs or packaging build could previously be merged, because `docs` and `build` fed nothing the gate read.
- Fail `just lint` on invisible and bidirectional control characters, which do not show up in review (Trojan Source, CVE-2021-42574).
- Add `timeout-minutes` to the `release.yml` and Dependabot workflow jobs, which were left unbounded when the CI jobs got theirs.
- Add `just release-check` to list `src/` changes against changelog entries before a release.
- Note in PACKAGING.md which `pyproject.toml` entries are django-marina only, so they are not synced into the siblings.
- Add an AI assistance policy to CONTRIBUTING.md, and say what this repo is for.
- Add a `CLAUDE.md` shim so Claude Code loads `AGENTS.md`, and trim `AGENTS.md`.

## 26.2 (2026-08-28)

- Drop support for Django 4.2 (EOL).
- Add support for Django 6.1.
- Store original media settings on runner instance instead of settings object (#652).
- Replace deprecated `DEFAULT_FILE_STORAGE` with `STORAGES` for Django 6.0 compatibility (#653).
- Support PUT, PATCH and DELETE in `ExtendedTestCase._response()` (#652).
- Add a maintenance-round section to MAINTAINING.md: check endoflife.date, reconcile the matrix, order release notes.
- Note in PACKAGING.md that django-bootstrap4/5 add GDAL steps to `ci.yml`.
- Add a 15-minute `timeout-minutes` to every CI job.
- Add `typos` spell checking to `just lint`.
- Note in PACKAGING.md that `[tool.check-manifest] ignore` is copied verbatim, and why.
- Add MAINTAINING.md (version-support policy, release process); add scope statement and PR-review checklist to CONTRIBUTING.md.
- Expand test coverage for `remove_attrs` (#652).
- Replace `USER_IGNORE = -1` magic sentinel with `object()` in `ExtendedClient` (#652).

## 26.1 (2026-01-02)

- Add tests (#634).
- Remove tests folder from coverage source (#631).
- Refactor release workflow to tag-based publishing via GitHub Actions (#629).
- Remove support for Django 5.1 (EOL) (#623).

## 25.3 (2025-11-14)

- Remove support for Python 3.9 (EOL) (#608, #611).
- Simplify justfile (#609).
- Exclude uv.lock from build (#605).
- Add support for Python 3.14 (#603).
- Add support for Django 6.0 (#602).

## 25.2 (2025-07-29)

- Add support for Django 5.2 (#587, #588).
- Drop support for Django 5.0 (#587, #588).
- Drop support for the Python 3.13 / Django 4.2 combination (#590).
- Use astral-sh/setup-uv in GitHub Actions (#593, #594).
- Build with `uv build` (#595).
- Use `uv.lock` in Github Actions (#596).

## 25.1 (2025-03-02)

- Fix Python versions in matrix (#583).
- Update .gitignore (#584).

## 24.3 (2024-12-10)

- Switch to just and uv for package management (#572).
- Add support for Python 3.13 (#572, #577).
- Drop support for Python 3.8 (EOL) (#571, #577).
- Add option to store test media in temp folder (#140).

## 24.2 (2024-04-16)

- Reinstate setuptools_scm for build (#441).

## 24.1 (2024-04-16)

- Remove support for Django 3.2 (EOL) (#439).
- Fix Read the Docs (#438).
- Remove setuptools_scm (#437).

## 23.7 (2023-12-28)

- Use setuptools-scm to build package (#402).

## 23.6 (2023-12-22)

- Use ruff instead of black for formatting (#392).
- Remove support for Python 3.7 (EOL) (#388).
- Revert packaging tools to setuptools, build, tox and twine (#394).

## 23.5 (2023-06-02)

- Improve and fix CI on GitHub Actions (#367, #374, #378).
- Reinstate coveralls (#369).
- Fix Read the Docs integration (#368).
- Update Sphinx and switch to Furo theme (#373).
- Remove references to tox and requirements (#383).
- Requirements in pyproject.toml (#380).

## 23.4 (2023-05-20)

- Switch build system to Hatch (#365).

## 23.3 (2023-04-28)

- Use ruff for linting and reformatting (#341).
- Update Makefile and package configuration (#339, #340).
- Drop support for Django 4.0 (EOL) (#352).
- Move version to source code, reduce dependencies (#351).

## 23.2 (2023-04-22)

- Replace m2r2 with sphinx-mdinclude (#335).
- Use setup.cfg instead of setup.py (#336).
- Tag version when publishing a release (#337).

## 23.1 (2023-04-14)

- Remove coveralls service (#328).
- Update requirements (#327).
- Add support for Python 3.11 and Django 4.2 (#328).

## 22.1 (2022-08-08)

- Drop support for Django 2.2 (EOL) (#220).
- Add support for Django 4.1 (#220).

## 21.2 (2021-12-27)

- Use Python's `http` module for status codes (#113).
- Drop support for Django 3.1 (EOL).
- Drop support for Python 3.6 (EOL).
- Fix CI.

## 21.1 (2021-11-18)

- Switch to a CalVer YY.MINOR versioning scheme. MINOR is the number of the release in the given year. This is the first release in 2021 using this scheme, so its version is 21.1. The next version this year will be 21.2. The first version in 2022 will be 22.1.
- Fix status code error message (#110).
- Add support for Django 4.0 and Python 3.10 (#82).
- Remove `pur` from developer requirements.

## 2.3.0 (2021-07-01)

- Allow `assertAllowed`, `assertForbidden`, `assertNotFound` to test for multiple users in a single call.
- Only allow user None to trigger logout.

## 2.2.0 (2021-04-28)

- Make `assertLoginRequired` test for redirect to `LOGIN_URL`.
- Improve Makefile build and publish commands.

## 2.1.0 (2021-04-13)

- Add `ExtendedTestCase.assertHasMessage` to test messages in response.
- Fix bug in ProtectedModelMixin.
- Add tests.

## 2.0.0 (2021-04-09)

- Add Dependabot.
- Revert to setuptools for packaging.
- Drop support for Django 3.0, extended support stopped on 2021-04-01).
- Add support for Django 3.2.

## 1.4.1 (2020-11-07)

- Fix CHANGELOG.

## 1.4.0 (2020-11-07)

- Reformat CHANGELOG.
- Add Python 3.9 to test matrix.
- Update Django 3.1 to non-development version in test matrix.
- Switch CI to GitHub Actions.
- Add docs and tests to sdist.

## 1.3.0 (2020-07-20)

- Add string argument to assertContainsSelector and assertNotContainsSelector in ExtendedTestCase.
- Add documentation on ExtendedTestCase.
- Package sphinx_rtd_theme is now properly installed as a `docs` extra.

## 1.2.0 (2020-07-05)

- Add Django 3.1 to test matrix.
- Fix coveralls.

## 1.1.0 (2020-06-17)

- Fix documentation on ReadTheDocs.
- Fix coveralls shield in README.
- Default branch of repository renamed `main`, related files have been updated.
- Update documentation and Sphinx configuration.
- Simplify imports and add tests.
- Update tox configuration.

## 1.0.0 (2020-06-14)

- Use [poetry](https://python-poetry.org) for managing dependencies and packaging.
- Extra test functions with `django_marina.test.clients.ExtendedClient` and `django_marina.test.test_cases.ExtendedTestCase`.
- Generic way to protect model instances against deletion using `django_marina.db.models.ProtectedModelMixin`.
- Skip migrations (useful in tests) with `django_marina.db.migrations.NoMigrations`.

## 0.0.2 (2019-06-10)

- Not meant for public release.

## 0.0.1 (2019-04-28)

- Not meant for public release.
