# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - [2020-06-17]
### Changed
- Fix documentation on ReadTheDocs.
- Fix coveralls shield in README.
- Default branch of repository renamed `main`, related files have been updated.
- Update documentation and Sphinx configuration.
- Simplify imports and add tests. 
- Update tox configuration.

## [1.0.0] - [2020-06-14]

### Added
- Use [poetry](https://python-poetry.org) for managing dependencies and packaging.
- Extra test functions with `django_marina.test.clients.ExtendedClient` and `django_marina.test.test_cases.ExtendedTestCase`.
- Generic way to protect model instances against deletion using `django_marina.db.models.ProtectedModelMixin`.
- Skip migrations (useful in tests) with `django_marina.db.migrations.NoMigrations`.

## [0.0.2] - 2019-06-10

### Summary
- Not meant for public release.

## [0.0.1] - 2019-04-28

### Summary
- Not meant for public release.
