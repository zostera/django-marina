from django.contrib.messages import get_messages
from django.test import TestCase

from .clients import ExtendedClient


class ExtendedTestCase(TestCase):
    """TestCase with a extended client and extra features for asserting response content."""

    HTTP_REDIRECT = 302
    HTTP_OK = 200
    HTTP_FORBIDDEN = 403
    HTTP_NOT_FOUND = 404

    client_class = ExtendedClient

    def _response(self, path, user, **kwargs):
        """Return response on a separate client instance, so without any side effects."""
        client = self.client_class()
        method = kwargs.pop("method", "get").lower()
        if method == "get":
            response = client.get(path, user=user, **kwargs)
        elif method == "post":
            response = client.post(path, user=user, **kwargs)
        else:
            raise AssertionError(f"Illegal value {method} for method, expected GET or POST")
        return response

    def assertResponseOk(self, response):
        """
        Assert that response has status HTTP_OK.

        :param response: HttpResponse
        """
        self.assertEqual(response.status_code, self.HTTP_OK, f"Response code should be HTTP_OK ({self.HTTP_OK})")

    def assertLoginRequired(self, path, **kwargs):
        """
        Make request while not logged in, assert that response has status HTTP_FORBIDDEN or HTTP_REDIRECTS.

        :param path: Path for request
        :param kwargs: Kwargs for request
        """
        response = self._response(path, user=None, **kwargs)
        # TODO: Check for proper redirection to login view
        self.assertIn(
            response.status_code,
            (self.HTTP_REDIRECT, self.HTTP_FORBIDDEN),
            (
                f"Response code should either be HTTP_REDIRECT ({self.HTTP_REDIRECT}) "
                f"or HTTP_FORBIDDEN ({self.HTTP_FORBIDDEN})"
            ),
        )

    def assertLoginNotRequired(self, path, **kwargs):
        """
        Make request while not logged in, assert that response has status HTTP_OK.

        :param path: Path for request
        :param kwargs: Kwargs for request
        """
        response = self._response(path, user=None, **kwargs)
        self.assertResponseOk(response)

    def assertAllowed(self, path, user, **kwargs):
        """
        Make request, assert that response has status HTTP_OK.

        Note that we use our own client so there are no side effects.

        :param path: Path for request
        :param user: User for request
        :param kwargs: Kwargs for request
        """
        response = self._response(path, user=user, **kwargs)
        self.assertResponseOk(response)

    def assertForbidden(self, path, user, **kwargs):
        """
        Make request, assert that response has status HTTP_FORBIDDEN.

        Note that we use our own client so there are no side effects.

        :param path: Path for request
        :param user: User for request
        :param kwargs: Kwargs for request
        """
        response = self._response(path, user=user, **kwargs)
        self.assertEqual(response.status_code, self.HTTP_FORBIDDEN)

    def assertNotFound(self, path, user, **kwargs):
        """
        Make request, assert that response has status HTTP_FORBIDDEN.

        Note that we use our own client so there are no side effects.

        :param path: Path for request
        :param user: User for request
        :param kwargs: Kwargs for request
        """
        response = self._response(path, user=user, **kwargs)
        self.assertEqual(response.status_code, self.HTTP_NOT_FOUND)

    def assertHasMessage(self, response, message):
        """
        Assert that response has given message.

        :param response: Response object
        :param message: Full text of message to check for
        """
        self.assertIn(message, [m.message for m in get_messages(response.wsgi_request)])

    def _assert_soup(self, response, soup_method, soup_args, soup_kwargs, status_code, count, msg_prefix):
        """Handle assertions that use BeautifulSoup, with interface similar to assertContains and assertNotContains."""
        if msg_prefix:
            msg_prefix = f"{msg_prefix}: "

        self.assertEqual(
            response.status_code,
            status_code,
            f"{msg_prefix}Couldn't retrieve content: Response code was {response.status_code} (expected {status_code})",
        )

        text_repr = f"{soup_args} {soup_kwargs}"

        # Extract string kwarg for selectors since soup does not implement it
        string = soup_kwargs.pop("string", None) if soup_method == "select" else None

        method = getattr(response.soup, soup_method)
        results = method(*soup_args, **soup_kwargs)

        # Search with string kwarg for selectors, by applying it to found tags
        if string is not None:
            results = [result for result in results if result.find(string=string)]

        real_count = len(results)

        if count == 0:  # No results should be found.
            self.assertEqual(real_count, 0, f"{msg_prefix}Response should not contain {text_repr}")
        elif count is None:  # At least one result should be found.
            self.assertTrue(real_count != 0, f"{msg_prefix}Couldn't find {text_repr} in response")
        else:  # Exactly this number of results should be found.
            self.assertEqual(
                real_count,
                count,
                f"{msg_prefix}Found {real_count} instances of {text_repr} in response (expected {count})",
            )

    def assertContainsTag(self, response, name=None, count=None, status_code=200, msg_prefix="", **kwargs):
        """
        Assert that tag can be found in response, using BeautifulSoup find notation.

        Documentation on tag finding: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kinds-of-filters
        """
        self._assert_soup(
            response,
            soup_method="find_all",
            soup_args=[name],
            soup_kwargs=kwargs,
            status_code=status_code,
            count=count,
            msg_prefix=msg_prefix,
        )

    def assertNotContainsTag(self, response, name=None, status_code=200, msg_prefix="", **kwargs):
        """
        Assert that tag cannot be found in response, using BeautifulSoup find notation.

        See `assertContainsTag` for documentation.
        """
        self._assert_soup(
            response,
            soup_method="find_all",
            soup_args=[name],
            soup_kwargs=kwargs,
            status_code=status_code,
            count=0,
            msg_prefix=msg_prefix,
        )

    def assertContainsSelector(self, response, selector, count=None, status_code=200, msg_prefix="", **kwargs):
        """
        Assert that CSS selector can be found in response.

        Documentation on CSS selectors:
        https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors

        To search within the found selectors, you can optionally provide a `string` argument. This will filter
        the found tags. See https://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-string-argument
        """
        self._assert_soup(
            response,
            soup_method="select",
            soup_args=[selector],
            soup_kwargs=kwargs,
            status_code=status_code,
            count=count,
            msg_prefix=msg_prefix,
        )

    def assertNotContainsSelector(self, response, selector, status_code=200, msg_prefix="", **kwargs):
        """Assert that CSS selector cannot be found in response."""
        self._assert_soup(
            response,
            soup_method="select",
            soup_args=[selector],
            soup_kwargs=kwargs,
            status_code=status_code,
            count=0,
            msg_prefix=msg_prefix,
        )
