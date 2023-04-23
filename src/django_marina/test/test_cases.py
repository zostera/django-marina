from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase

from .clients import ExtendedClient


def _login_url(next):
    """Return login url that Django uses in its redirect to login."""
    from django.contrib.auth.views import redirect_to_login

    redirect_response = redirect_to_login(next)
    return redirect_response["Location"]


def _msg_prefix_add(msg_prefix, value):
    """Return msg_prefix with added value."""
    msg_prefix = f"{msg_prefix}: " if msg_prefix else ""
    return f"{msg_prefix}{value}"


class ExtendedTestCase(TestCase):
    """TestCase with a extended client and extra features for asserting response content."""

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
            raise AssertionError(f"Invalid method {method} (expected GET or POST).")
        return response

    def assertResponseStatusCode(self, response, status_code, msg_prefix=None):
        """
        Assert that response has given status code.

        :param response: HttpResponse
        :param status_code: int
        :param msg_prefix: str
        """
        self.assertEqual(
            response.status_code,
            status_code,
            _msg_prefix_add(msg_prefix, f"Invalid response code {response.status_code} (expected {status_code})."),
        )

    def assertResponseOk(self, response):
        """
        Assert that response has status code OK.

        :param response: HttpResponse
        """
        self.assertResponseStatusCode(response, HTTPStatus.OK)

    def assertLoginRequired(self, path, **kwargs):
        """
        Make request while not logged in, assert that response has status code Forbidden or redirects to login page.

        :param path: Path for request
        :param kwargs: Kwargs for request
        """
        response = self._response(path, user=None, **kwargs)
        if response.status_code == HTTPStatus.FOUND:
            self.assertRedirects(response, _login_url(path))
        else:
            self.assertResponseStatusCode(response, HTTPStatus.FORBIDDEN)

    def _assertStatusCode(self, path, user, status_code, msg_prefix=None, **kwargs):
        """
        Make request, assert that response has given status code.

        :param path: Path for request
        :param user: User for request
        :param kwargs: Kwargs for request
        """
        users = user if isinstance(user, (list, tuple)) else [user]
        for user in users:
            response = self._response(path, user=user, **kwargs)
            self.assertResponseStatusCode(response, status_code, _msg_prefix_add(msg_prefix, user))

    def assertLoginNotRequired(self, path, **kwargs):
        """
        Make request while not logged in, assert that response has status code OK.

        :param path: Path for request
        :param kwargs: Kwargs for request
        """
        self._assertStatusCode(path, user=None, status_code=HTTPStatus.OK, **kwargs)

    def assertAllowed(self, path, user, **kwargs):
        """
        Make request, assert that response has status code OK.

        If `user` contains a list of users, the assertion will be made for every user in that list.

        :param path: Path for request
        :param user: User or list of users for request
        :param kwargs: Kwargs for request
        """
        self._assertStatusCode(path, user=user, status_code=HTTPStatus.OK, **kwargs)

    def assertForbidden(self, path, user, **kwargs):
        """
        Make request, assert that response has status code Forbidden.

        If `user` contains a list of users, the assertion will be made for every user in that list.

        :param path: Path for request
        :param user: User or list of users for request
        :param kwargs: Kwargs for request
        """
        self._assertStatusCode(path, user=user, status_code=HTTPStatus.FORBIDDEN, **kwargs)

    def assertNotFound(self, path, user, **kwargs):
        """
        Make request, assert that response has status code Not Found.

        If `user` contains a list of users, the assertion will be made for every user in that list.

        :param path: Path for request
        :param user: User or list of users for request
        :param kwargs: Kwargs for request
        """
        self._assertStatusCode(path, user=user, status_code=HTTPStatus.NOT_FOUND, **kwargs)

    def assertHasMessage(self, response, message):
        """
        Assert that response has given message.

        :param response: Response object
        :param message: Full text of message to check for
        """
        self.assertIn(message, [m.message for m in get_messages(response.wsgi_request)])

    def _get_soup_num_results(self, response, soup_method, soup_args, soup_kwargs):
        """Get number of results in response for BeautifulSoup query."""
        # Extract string kwarg for selectors since soup does not implement it
        string = soup_kwargs.pop("string", None) if soup_method == "select" else None

        method = getattr(response.soup, soup_method)
        results = method(*soup_args, **soup_kwargs)

        # Search with string kwarg for selectors, by applying it to found tags
        if string is not None:
            results = [result for result in results if result.find(string=string)]

        return len(results)

    def _assert_soup(self, response, soup_method, soup_args, soup_kwargs, status_code, count, msg_prefix):
        """Handle assertions that use BeautifulSoup, with interface similar to assertContains and assertNotContains."""
        self.assertEqual(
            response.status_code,
            status_code,
            _msg_prefix_add(
                msg_prefix,
                f"Couldn't retrieve content: Response code was {response.status_code} (expected {status_code}).",
            ),
        )

        soup_query = f"{soup_args} {soup_kwargs}"
        num_results = self._get_soup_num_results(response, soup_method, soup_args, soup_kwargs)

        if count == 0:
            self.assertEqual(num_results, 0, _msg_prefix_add(msg_prefix, f"Response should not contain {soup_query}"))
        elif count is None:
            self.assertTrue(num_results != 0, _msg_prefix_add(msg_prefix, f"Couldn't find {soup_query} in response"))
        else:
            self.assertEqual(
                num_results,
                count,
                _msg_prefix_add(
                    msg_prefix, f"Found {num_results} instances of {soup_query} in response (expected {count})"
                ),
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

        Documentation on CSS selectors: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors

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
