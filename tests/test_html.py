from django.test import TestCase

from django_marina.html import remove_attrs


class HtmlTestCase(TestCase):
    def test_remove_attrs(self):
        self.assertEqual(remove_attrs('<span foo="bar"></span>', ["foo"]), "<span></span>")

    def test_remove_attrs_none_html(self):
        self.assertIsNone(remove_attrs(None, ["foo"]))

    def test_remove_attrs_empty_string(self):
        self.assertEqual(remove_attrs("", ["foo"]), "")

    def test_remove_attrs_none_attrs(self):
        self.assertEqual(remove_attrs('<span foo="bar"></span>', None), '<span foo="bar"></span>')

    def test_remove_attrs_empty_attrs(self):
        self.assertEqual(remove_attrs('<span foo="bar"></span>', []), '<span foo="bar"></span>')

    def test_remove_attrs_multiple(self):
        self.assertEqual(remove_attrs('<span foo="1" bar="2"></span>', ["foo", "bar"]), "<span></span>")

    def test_remove_attrs_nonexistent(self):
        self.assertEqual(remove_attrs('<span foo="bar"></span>', ["baz"]), '<span foo="bar"></span>')
