from django.test import TestCase


class ImportDbTestCase(TestCase):
    def test_import_disable_migrations(self):
        from django_marina.db import DisableMigrations  # noqa

    def test_import_protected_model_mixin(self):
        from django_marina.db import ProtectedModelMixin  # noqa


class ImportTestTestCase(TestCase):
    def test_import_extended_client(self):
        from django_marina.test import ExtendedClient  # noqa

    def test_import_extended_test_case(self):
        from django_marina.test import ExtendedTestCase  # noqa
