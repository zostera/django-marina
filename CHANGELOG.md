# Changelog

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
