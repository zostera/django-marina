"""
A standalone test runner script, configuring the minimum settings
required for django-marina tests to execute.

Re-use at your own risk: many Django applications will require full
settings and/or templates in order to execute their tests, while
django-marina does not.

Adapted from James Bennett's https://github.com/ubernostrum/pwned-passwords-django

"""

import os
import sys

# Make sure the app is (at least temporarily) on the import path.
APP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, APP_DIR)

# Technically, django-marina does not require any of these
# settings; it doesn't even need to be in INSTALLED_APPS in order to
# work.
#
# However, Django itself requires DATABASES and ROOT_URLCONF to be
# set, Django's system-check framework will raise warnings if no value
# is provided for MIDDLEWARE, and the Django test runner needs your
# app to be in INSTALLED_APPS in order to work.
SETTINGS_DICT = {
    "INSTALLED_APPS": (
        "django.contrib.contenttypes",
        "django.contrib.auth",
        "django.contrib.sessions",
        "marina",
    ),
    "ROOT_URLCONF": "tests.urls",
    "DATABASES": {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
    },
    "MIDDLEWARE": (
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ),
}


def run_tests():
    # Making Django run this way is a two-step process. First, call
    # settings.configure() to give Django settings to work with:
    from django.conf import settings

    settings.configure(**SETTINGS_DICT)

    # Then, call django.setup() to initialize the application registry
    # and other bits:
    import django

    django.setup()

    # Now we instantiate a test runner...
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)

    # And then we run tests and return the results.
    test_runner = TestRunner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(["tests"])
    sys.exit(failures)


if __name__ == "__main__":
    run_tests()
