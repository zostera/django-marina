from django.contrib.auth import get_user_model
from django.test import TestCase

from marina.test.clients import ClientWithFetch


User = get_user_model()


class BaseViewsTestCase(TestCase):
    """
    Provides often used tests for urls."""

    HTTP_REDIRECT = 302
    HTTP_OK = 200
    HTTP_FORBIDDEN = 403

    client_class = ClientWithFetch

    def assertLoginNotRequired(self, url, **kwargs):
        """
        Logout, fetch response for url, assert that response has status HTTP_OK.

        Note that we use our own client so there are no side effects.

        :param url: Url to fetch
        :param kwargs: Kwargs to fetch url
        """
        client = self.client_class()
        response = client.fetch(url, user=None, **kwargs)
        self.assertEqual(
            response.status_code,
            self.HTTP_OK,
            f"response should be status ok ({self.HTTP_OK})",
        )

    def assertLoginRequired(self, url, **kwargs):
        """
        Logout, fetch response for url, assert that response has status HTTP_FORBIDDEN or redirects to the login page.

        Note that we use our own client so there are no side effects.

        :param url: Url to fetch
        :param kwargs: Kwargs to fetch url
        """
        client = self.client_class()
        response = client.fetch(url, user=None, **kwargs)
        # TODO: Check for proper redirection to login URL, maybe use assertRedirects
        self.assertIn(
            response.status_code,
            (self.HTTP_REDIRECT, self.HTTP_FORBIDDEN),
            f"response should either be redirect ({self.HTTP_REDIRECT}) or return forbidden ({self.HTTP_FORBIDDEN})",
        )

    def assertAllowed(self, url, user, **kwargs):
        """
        Logout, fetch response for url, assert that response has status HTTP_OK.

        Note that we use our own client so there are no side effects.

        :param url: Url to fetch
        :param user: User to fetch url
        :param kwargs: Kwargs to fetch url
        """
        client = self.client_class()
        response = client.fetch(url, user=user, **kwargs)
        self.assertResponseOk(response)

    def assertResponseOk(self, response):
        """
        Assert that response has status HTTP_OK.

        :param response: HttpResponse
        """
        self.assertEqual(response.status_code, self.HTTP_OK)

    def assertForbidden(self, url, user, **kwargs):
        """
        Logout, fetch response for url, assert that response has status HTTP_FORBIDDEN.

        Note that we use our own client so there are no side effects.

        :param url: Url to fetch
        :param user: User to fetch url
        :param kwargs: Kwargs to fetch url
        """
        client = self.client_class()
        response = client.fetch(url, user=user, **kwargs)
        self.assertEqual(response.status_code, self.HTTP_FORBIDDEN)
