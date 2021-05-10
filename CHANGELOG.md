# Changelog

## In development

- Allow `assertAllowed`, `assertForbidden`, `assertNotFound` to test for multiple users in a single call.

## 2.2.0 - 2021-04-28

- Make `assertLoginRequired` test for redirect to `LOGIN_URL`.
- Improve Makefile build and publish commands.

## 2.1.0 - 2021-04-13

- Add `ExtendedTestCase.assertHasMessage` to test messages in response.
- Fix bug in ProtectedModelMixin.
- Add tests.

## 2.0.0 - 2021-04-09

- Add Dependabot.
- Revert to setuptools for packaging.
- Drop support for Django 3.0, extended support stopped on 2021-04-01).
- Add support for Django 3.2.

## 1.4.1 - 2020-11-07

- Fix CHANGELOG.

## 1.4.0 - 2020-11-07

- Reformat CHANGELOG.
- Add Python 3.9 to test matrix.
- Update Django 3.1 to non-development version in test matrix.
- Switch CI to GitHub Actions.
- Add docs and tests to sdist.

## 1.3.0 - 2020-07-20

- Add string argument to assertContainsSelector and assertNotContainsSelector in ExtendedTestCase.
- Add documentation on ExtendedTestCase.
- Package sphinx_rtd_theme is now properly installed as a `docs` extra.

## 1.2.0 - 2020-07-05

- Add Django 3.1 to test matrix.
- Fix coveralls.

## 1.1.0 - 2020-06-17

- Fix documentation on ReadTheDocs.
- Fix coveralls shield in README.
- Default branch of repository renamed `main`, related files have been updated.
- Update documentation and Sphinx configuration.
- Simplify imports and add tests. 
- Update tox configuration.

## 1.0.0 - 2020-06-14

- Use [poetry](https://python-poetry.org) for managing dependencies and packaging.
- Extra test functions with `django_marina.test.clients.ExtendedClient` and `django_marina.test.test_cases.ExtendedTestCase`.
- Generic way to protect model instances against deletion using `django_marina.db.models.ProtectedModelMixin`.
- Skip migrations (useful in tests) with `django_marina.db.migrations.NoMigrations`.

## 0.0.2 - 2019-06-10

- Not meant for public release.

## 0.0.1 - 2019-04-28

- Not meant for public release.
