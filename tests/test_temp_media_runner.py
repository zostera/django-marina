import os

from django.conf import settings
from django.test import SimpleTestCase, override_settings

from django_marina.test.runners import TempMediaMixin


class _NoopRunner:
    def setup_test_environment(self):
        pass

    def teardown_test_environment(self):
        pass


class _TempMediaRunner(TempMediaMixin, _NoopRunner):
    pass


class TempMediaDiscoverRunnerTestCase(SimpleTestCase):
    @override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
    def test_temp_media_setup_and_teardown(self):
        runner = _TempMediaRunner()
        original_media_root = settings.MEDIA_ROOT
        original_storage = settings.DEFAULT_FILE_STORAGE

        runner.setup_test_environment()
        try:
            self.assertTrue(os.path.isdir(settings.MEDIA_ROOT))
            self.assertNotEqual(settings.MEDIA_ROOT, original_media_root)
            self.assertEqual(
                settings.DEFAULT_FILE_STORAGE,
                "django.core.files.storage.FileSystemStorage",
            )
            self.assertTrue(hasattr(settings, "_original_media_root"))
            self.assertTrue(hasattr(settings, "_original_file_storage"))
        finally:
            temp_media_root = runner._temp_media
            runner.teardown_test_environment()

        self.assertEqual(settings.MEDIA_ROOT, original_media_root)
        self.assertEqual(settings.DEFAULT_FILE_STORAGE, original_storage)
        self.assertFalse(hasattr(settings, "_original_media_root"))
        self.assertFalse(hasattr(settings, "_original_file_storage"))
        self.assertFalse(os.path.exists(temp_media_root))
