from django.core.exceptions import PermissionDenied
from django.test import TestCase

from django_marina.db import DisableMigrations

from .models import ProtectedModel


class ProtectedModelMixinTestCase(TestCase):
    def test_update_protected(self):
        protected = ProtectedModel(name="protected", is_update_protected=True)
        protected.save()
        with self.assertRaises(PermissionDenied):
            protected.save()

    def test_update_unprotected(self):
        unprotected = ProtectedModel(name="protected", is_update_protected=False)
        unprotected.save()
        unprotected.name = "changed"
        unprotected.save()
        self.assertEqual(unprotected.name, "changed")

    def test_get_protected_against_update_message(self):
        protected = ProtectedModel(name="protected", is_update_protected=True)
        protected.save()
        message = protected.get_update_protection_message()
        self.assertEqual(message, "This object has update protection.")

    def test_delete_protected(self):
        protected = ProtectedModel(name="protected", is_delete_protected=True)
        protected.save()
        with self.assertRaises(PermissionDenied):
            protected.delete()

    def test_delete_unprotected(self):
        unprotected = ProtectedModel(name="protected", is_delete_protected=False)
        unprotected.save()
        unprotected.delete()
        self.assertIsNone(ProtectedModel.objects.filter(pk=unprotected.pk).first())

    def test_get_protected_against_delete_message(self):
        protected = ProtectedModel(name="protected", is_delete_protected=True)
        protected.save()
        message = protected.get_delete_protection_message()
        self.assertEqual(message, "This object has delete protection.")


class DisableMigrationsTestCase(TestCase):
    def test_disable_migrations(self):
        instance = DisableMigrations()
        self.assertTrue("anything" in instance)
        self.assertIsNone(instance["anything"])
