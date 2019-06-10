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
    HTTP_NOT_FOUND = 404

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

    def assertResponseStatusCode(self, response, status_code):
        """
        Assert that response has specified status.

        :param response: HttpResponse
        :param status: Required status
        """
        self.assertEqual(response.status_code, status_code)

    def assertResponseOk(self, response):
        """
        Assert that response has status HTTP_OK.

        :param response: HttpResponse
        """
        self.assertResponseStatusCode(response, self.HTTP_OK)

    def assertResponseForbidden(self, response):
        """
        Assert that response has status HTTP_FORBIDDEN.

        :param response: HttpResponse
        """
        self.assertResponseStatusCode(response, self.HTTP_FORBIDDEN)

    def assertResponseNotFound(self, response):
        """
        Assert that response has status HTTP_NOT_FOUND.

        :param response: HttpResponse
        """
        self.assertResponseStatusCode(response, self.HTTP_NOT_FOUND)

    def assertStatusCode(self, url, user, status_code, **kwargs):
        """
        Logout, fetch response for url, assert that response has specified status.

        Note that we use our own client so there are no side effects.

        :param url: Url to fetch
        :param user: User to fetch url
        :param status_code: Required status
        :param kwargs: Kwargs to fetch url
        """
        client = self.client_class()
        response = client.fetch(url, user=user, **kwargs)
        self.assertResponseStatusCode(response, status_code)

    def assertAllowed(self, url, user, **kwargs):
        """
        Logout, fetch response for url, assert that response has status HTTP_OK.

        Note that we use our own client so there are no side effects.

        :param url: Url to fetch
        :param user: User to fetch url
        :param kwargs: Kwargs to fetch url
        """
        kwargs["status_code"] = self.HTTP_OK
        self.assertStatusCode(url, user, **kwargs)

    def assertForbidden(self, url, user, **kwargs):
        """
        Logout, fetch response for url, assert that response has status HTTP_FORBIDDEN.

        Note that we use our own client so there are no side effects.

        :param url: Url to fetch
        :param user: User to fetch url
        :param kwargs: Kwargs to fetch url
        """
        kwargs["status_code"] = self.HTTP_FORBIDDEN
        self.assertStatusCode(url, user, **kwargs)

    def assertNotFound(self, url, user, **kwargs):
        """
        Logout, fetch response for url, assert that response has status HTTP_NOT_FOUND.

        Note that we use our own client so there are no side effects.

        :param url: Url to fetch
        :param user: User to fetch url
        :param kwargs: Kwargs to fetch url
        """
        kwargs["status_code"] = self.HTTP_NOT_FOUND
        self.assertStatusCode(url, user, **kwargs)
