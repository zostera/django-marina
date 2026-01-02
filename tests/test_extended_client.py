from django.template import engines
from django.template.response import SimpleTemplateResponse
from django.test import TestCase
from django.urls import reverse

from django_marina.test import ExtendedClient
from django_marina.test.clients import _get_soup


class ExtendedClientTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url_echo = reverse("echo")

    def test_get(self):
        client = ExtendedClient()
        response = client.get(f"{self.url_echo}?foo=bar")
        self.assertContains(response, "foo")
        self.assertContains(response, "bar")

    def test_post(self):
        client = ExtendedClient()
        response = client.post(self.url_echo, data={"foo": "bar"})
        self.assertContains(response, "foo")
        self.assertContains(response, "bar")

    def test_get_soup_renders_template_response(self):
        template = engines["django"].from_string("<html><body><p>Hello</p></body></html>")
        response = SimpleTemplateResponse(template=template, context={})
        self.assertFalse(response.is_rendered)
        soup = _get_soup(response)
        self.assertTrue(response.is_rendered)
        self.assertEqual(soup.p.text, "Hello")
