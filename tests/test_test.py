from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from marina.test.clients import ClientWithFetch
from marina.test.test_cases import BaseViewsTestCase


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


class BaseViewsTestCaseTestCase(BaseViewsTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.echo_url = reverse("echo")
        cls.user = mommy.make(User)
        cls.anonymous = AnonymousUser()
        cls.superuser = mommy.make(User, is_superuser=True)
        cls.url_public = reverse("echo")
        cls.url_authenticated = reverse("logged_in_only")
        cls.url_superuser = reverse("superuser_only")

    def test_assertLoginNotRequired(self):
        self.assertLoginNotRequired(url=self.url_public)
        with self.assertRaises(AssertionError):
            self.assertLoginNotRequired(url=self.url_authenticated)
        with self.assertRaises(AssertionError):
            self.assertLoginNotRequired(url=self.url_superuser)

    def test_assertLoginRequired(self):
        with self.assertRaises(AssertionError):
            self.assertLoginRequired(url=self.url_public)
        self.assertLoginRequired(url=self.url_authenticated)
        self.assertLoginRequired(url=self.url_superuser)

    def test_assertAllowed(self):
        self.assertAllowed(url=self.url_public, user=None)
        self.assertAllowed(url=self.url_public, user=self.user)
        self.assertAllowed(url=self.url_public, user=self.superuser)

        with self.assertRaises(AssertionError):
            self.assertAllowed(url=self.url_authenticated, user=None)
        self.assertAllowed(url=self.url_authenticated, user=self.user)
        self.assertAllowed(url=self.url_authenticated, user=self.superuser)

        with self.assertRaises(AssertionError):
            self.assertAllowed(url=self.url_superuser, user=None)
        with self.assertRaises(AssertionError):
            self.assertAllowed(url=self.url_superuser, user=self.user)
        self.assertAllowed(url=self.url_superuser, user=self.superuser)

    def test_assertForbidden(self):
        with self.assertRaises(AssertionError):
            self.assertForbidden(url=self.url_public, user=None)
        with self.assertRaises(AssertionError):
            self.assertForbidden(url=self.url_public, user=self.user)
        with self.assertRaises(AssertionError):
            self.assertForbidden(url=self.url_public, user=self.superuser)

        with self.assertRaises(AssertionError):
            # This will raise Redirect, not Forbidden
            self.assertForbidden(url=self.url_authenticated, user=None)
        with self.assertRaises(AssertionError):
            self.assertForbidden(url=self.url_authenticated, user=self.user)
        with self.assertRaises(AssertionError):
            self.assertForbidden(url=self.url_authenticated, user=self.superuser)

        self.assertForbidden(url=self.url_superuser, user=None)
        self.assertForbidden(url=self.url_superuser, user=self.user)
        with self.assertRaises(AssertionError):
            self.assertForbidden(url=self.url_superuser, user=self.superuser)
