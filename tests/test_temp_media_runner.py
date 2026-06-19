import os

from django.conf import settings
from django.test import SimpleTestCase

from django_marina.test.runners import TempMediaMixin


class _NoopRunner:
    def setup_test_environment(self):
        pass

    def teardown_test_environment(self):
        pass


class _TempMediaRunner(TempMediaMixin, _NoopRunner):
    pass


class TempMediaDiscoverRunnerTestCase(SimpleTestCase):
    def test_temp_media_setup_and_teardown(self):
        runner = _TempMediaRunner()
        original_media_root = settings.MEDIA_ROOT
        original_storages = settings.STORAGES.copy()

        runner.setup_test_environment()
        try:
            self.assertTrue(os.path.isdir(settings.MEDIA_ROOT))
            self.assertNotEqual(settings.MEDIA_ROOT, original_media_root)
            self.assertEqual(
                settings.STORAGES["default"]["BACKEND"],
                "django.core.files.storage.FileSystemStorage",
            )
            self.assertEqual(runner._original_media_root, original_media_root)
            self.assertEqual(runner._original_storages, original_storages)
        finally:
            temp_media_root = runner._temp_media
            runner.teardown_test_environment()

        self.assertEqual(settings.MEDIA_ROOT, original_media_root)
        self.assertEqual(settings.STORAGES, original_storages)
        self.assertFalse(os.path.exists(temp_media_root))
