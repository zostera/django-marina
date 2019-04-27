from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from marina.test.clients import ClientWithFetch


User = get_user_model()


class ClientWithFetchTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.echo_url = reverse("echo")
        cls.user = mommy.make(User)
        cls.anonymous = AnonymousUser()

    def test_user_is_required(self):
        client = ClientWithFetch()
        with self.assertRaises(TypeError):
            client.fetch(self.echo_url)

    def test_user_none_is_allowed(self):
        client = ClientWithFetch()
        response = client.fetch(self.echo_url, user=None)
        self.assertEqual(response.status_code, 200)

    def test_user_anonymous_is_not_allowed(self):
        client = ClientWithFetch()
        with self.assertRaises(Exception):
            client.fetch(self.echo_url, user=self.anonymous)

    def test_user_user_is_allowed(self):
        client = ClientWithFetch()
        response = client.fetch(self.echo_url, user=self.user)
        self.assertEqual(response.status_code, 200)

    def test_method_is_not_required(self):
        client = ClientWithFetch()
        response = client.fetch(self.echo_url, user=None)
        self.assertEqual(response.status_code, 200)

    def test_method_GET_is_allowed(self):
        client = ClientWithFetch()
        response = client.fetch(self.echo_url, method="GET", user=None)
        self.assertEqual(response.status_code, 200)

    def test_method_POST_is_allowed(self):
        client = ClientWithFetch()
        response = client.fetch(self.echo_url, method="POST", user=None)
        self.assertEqual(response.status_code, 200)

    def test_method_FOO_is_not_allowed(self):
        client = ClientWithFetch()
        with self.assertRaises(ValueError):
            client.fetch(self.echo_url, method="FOO", user=None)
