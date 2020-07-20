import re

from django.contrib.auth.models import User
from django.urls import reverse

from django_marina.test import ExtendedTestCase


class ExtendedTestCaseTestCase(ExtendedTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url_access_all = reverse("home")
        cls.url_access_authenticated = reverse("access_authenticated")
        cls.url_access_superuser = reverse("access_superuser")
        cls.url_does_not_exist = "/does-not-exist"
        cls.user = User(username="user", is_superuser=False)
        cls.user.save()
        cls.superuser = User(username="superuser", is_superuser=True)
        cls.superuser.save()

    def test_assert_response_ok(self):
        response = self.client.get(self.url_access_all)
        self.assertResponseOk(response)
        response = self.client.get(self.url_does_not_exist)
        with self.assertRaises(AssertionError):
            self.assertResponseOk(response)

    def test_assert_login_required(self):
        self.assertLoginRequired(self.url_access_authenticated)
        with self.assertRaises(AssertionError):
            self.assertLoginRequired(self.url_access_all)

    def test_assert_login_not_required(self):
        self.assertLoginNotRequired(reverse("home"))
        with self.assertRaises(AssertionError):
            self.assertLoginNotRequired(self.url_access_authenticated)

    def test_assert_allowed(self):
        self.assertAllowed(self.url_access_all, user=None)
        self.assertAllowed(self.url_access_all, user=self.user)
        self.assertAllowed(self.url_access_all, user=self.superuser)

        self.assertAllowed(self.url_access_authenticated, user=self.user)
        self.assertAllowed(self.url_access_authenticated, user=self.superuser)
        with self.assertRaises(AssertionError):
            self.assertAllowed(self.url_access_authenticated, user=None)

        self.assertAllowed(self.url_access_superuser, user=self.superuser)
        with self.assertRaises(AssertionError):
            self.assertAllowed(self.url_access_superuser, user=None)
        with self.assertRaises(AssertionError):
            self.assertAllowed(self.url_access_superuser, user=self.user)

    def test_assert_forbidden(self):
        with self.assertRaises(AssertionError):
            self.assertForbidden(self.url_access_all, user=None)
        with self.assertRaises(AssertionError):
            self.assertForbidden(self.url_access_all, user=self.user)
        with self.assertRaises(AssertionError):
            self.assertForbidden(self.url_access_all, user=self.superuser)

        with self.assertRaises(AssertionError):
            # Be careful with assertForbidden and user=None, if login is required you may get either
            # HTTP_FORBIDDEN or HTTP_REDIRECT. In this test, we will get HTTP_REDIRECT.
            self.assertForbidden(self.url_access_authenticated, user=None)
        with self.assertRaises(AssertionError):
            self.assertForbidden(self.url_access_authenticated, user=self.user)
        with self.assertRaises(AssertionError):
            self.assertForbidden(self.url_access_authenticated, user=self.superuser)

        with self.assertRaises(AssertionError):
            self.assertForbidden(self.url_access_superuser, user=None)
        self.assertForbidden(self.url_access_superuser, user=self.user)
        with self.assertRaises(AssertionError):
            self.assertForbidden(self.url_access_superuser, user=self.superuser)

    def test_assert_not_found(self):
        self.assertNotFound(self.url_does_not_exist, user=None)
        self.assertNotFound(self.url_does_not_exist, user=self.user)
        self.assertNotFound(self.url_does_not_exist, user=self.superuser)
        with self.assertRaises(AssertionError):
            self.assertNotFound(self.url_access_all, user=None)
        with self.assertRaises(AssertionError):
            self.assertNotFound(self.url_access_all, user=self.user)
        with self.assertRaises(AssertionError):
            self.assertNotFound(self.url_access_all, user=self.superuser)

    def test_assert_contains_tag(self):
        response = self.client.get(self.url_access_all)
        self.assertContainsTag(response, "h1")
        with self.assertRaises(AssertionError):
            self.assertContainsTag(response, "h2")

    def test_assert_not_contains_tag(self):
        response = self.client.get(self.url_access_all)
        self.assertNotContainsTag(response, "h2")
        with self.assertRaises(AssertionError):
            self.assertNotContainsTag(response, "h1")

    def test_assert_contains_selector(self):
        response = self.client.get(self.url_access_all)
        self.assertContainsSelector(response, "body h1")
        with self.assertRaises(AssertionError):
            self.assertContainsSelector(response, "body h1 a")

    def test_assert_not_contains_selector(self):
        response = self.client.get(self.url_access_all)
        self.assertNotContainsSelector(response, "body h1 a")
        with self.assertRaises(AssertionError):
            self.assertNotContainsSelector(response, "body h1")

    def test_assert_tag_with_string(self):
        response = self.client.get(self.url_access_all)
        self.assertNotContainsTag(response, "h1", string="Goodbye World!")
        self.assertContainsTag(response, "h1", string="Hello World!")
        self.assertNotContainsTag(response, "h1", string="Hello")
        self.assertContainsTag(response, "h1", string=re.compile("Hello"))

    def test_assert_selector_with_string(self):
        response = self.client.get(self.url_access_all)
        self.assertNotContainsSelector(response, "h1", string="Goodbye World!")
        self.assertContainsSelector(response, "h1", string="Hello World!")
        self.assertNotContainsSelector(response, "h1", string="Hello")
        self.assertContainsSelector(response, "h1", string=re.compile("Hello"))
