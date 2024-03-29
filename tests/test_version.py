from django.test import TestCase


class VersionTest(TestCase):
    """Test presence of package version."""

    def test_version(self):
        import django_marina

        version = django_marina.__version__
        version_parts = version.split(".")
        self.assertTrue(len(version_parts) in (2, 3))
