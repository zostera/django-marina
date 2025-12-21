import sys

from django.test import TestCase


class VersionTest(TestCase):
    """Test presence of package version."""

    def test_version(self):
        import django_marina

        version = django_marina.__version__
        version_parts = version.split(".")
        self.assertTrue(len(version_parts) in (2, 3))

        try:
            import django

            django_version = django.get_version()
        except Exception:
            django_version = "not available"

        if "test" in sys.argv:
            print(f"* Python {sys.version.split()[0]}\n* Django {django_version}")
