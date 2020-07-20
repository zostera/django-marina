from django.test import TestCase
from django.urls import reverse

from django_marina.test import ExtendedClient


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
