from django.test import TestCase

from django_marina.html import remove_attrs


class HtmlTestCase(TestCase):
    def test_remove_attrs(self):
        self.assertEqual(remove_attrs('<span foo="bar"></span>', ["foo"]), "<span></span>")
