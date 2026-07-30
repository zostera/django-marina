# django-marina

[![CI](https://github.com/zostera/django-marina/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zostera/django-marina/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/zostera/django-marina/badge.svg?branch=main)](https://coveralls.io/github/zostera/django-marina?branch=main)
[![Latest PyPI version](https://img.shields.io/pypi/v/django-marina.svg)](https://pypi.python.org/pypi/django-marina)

Django extensions by Zostera.

## Goal

The goal of this project is to bundle small, reusable extensions for Django projects: database
utilities, HTML helpers, and test infrastructure shared across Zostera's Django packages.

## Status

Ready for production. Issues and pull requests welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Requirements

This package requires a combination of Python and Django that is currently supported.

See "Supported Versions" on https://www.djangoproject.com/download/.

This package uses [uv](https://github.com/astral-sh/uv) and [just](https://github.com/casey/just) for local development.

## Documentation

The full documentation is at https://django-marina.readthedocs.io/

## Installation

1. Install using pip:

    ```console
    pip install django-marina
    ```

2. Add to `INSTALLED_APPS` in your `settings.py`:

   ```python
   INSTALLED_APPS = (
       # ...
       "django_marina",
       # ...
   )
   ```

## Bugs and suggestions

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/zostera/django-marina/issues

## License

You can use this under BSD-3-Clause. See [LICENSE](LICENSE) file for details.

## Author

Developed and maintained by [Zostera](https://zostera.nl).

Original author: [Dylan Verheul](https://github.com/dyve).

Thanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.

Please see [AUTHORS](AUTHORS) for a list of contributors.
