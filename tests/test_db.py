from django.core.exceptions import PermissionDenied
from django.test import TestCase

from django_marina.db import DisableMigrations

from .models import ProtectedModel


class ProtectedModelMixinTestCase(TestCase):
    def test_delete_protected(self):
        protected = ProtectedModel(name="protected")
        protected.save()
        self.assertIsNotNone(ProtectedModel.objects.filter(pk=protected.pk).first())
        with self.assertRaises(PermissionDenied):
            protected.delete()

    def test_delete_unprotected(self):
        protected = ProtectedModel(name="protected", is_protected=False)
        protected.save()
        self.assertIsNotNone(ProtectedModel.objects.filter(pk=protected.pk).first())
        protected.delete()
        self.assertIsNone(ProtectedModel.objects.filter(pk=protected.pk).first())

    def test_get_protected_against_delete_message(self):
        protected = ProtectedModel(name="protected")
        protected.save()
        message = protected.get_protected_against_deletion_message()
        self.assertEqual(message, "This object is protected against deletion.")


class DisableMigrationsTestCase(TestCase):
    def test_disable_migrations(self):
        instance = DisableMigrations()
        self.assertTrue("anything" in instance)
        self.assertIsNone(instance["anything"])
