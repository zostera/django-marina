import logging

logger = logging.getLogger(__name__)


class DisableMigrations(object):
    """
    Settings class to disable migrations.

    In your `settings_test.py` you can set MIGRATION_MODULES, for example:

    .. code-block:: python

      from django_marina.db import DisableMigrations

      if some_condition:
          MIGRATION_MODULES = DisableMigrations()
    """

    # Based on: https://simpleisbetterthancomplex.com/tips/2016/08/19/django-tip-12-disabling-migrations-to-speed-up-unit-tests.html  # NOQA
    def __init__(self, *args, **kwargs):
        logger.debug("Migrations disabled.")

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None
