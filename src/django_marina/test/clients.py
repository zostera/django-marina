from bs4 import BeautifulSoup
from django.test import Client
from django.utils.functional import SimpleLazyObject


def _get_soup(response):
    """Return soup for response."""
    if hasattr(response, "render") and callable(response.render) and not response.is_rendered:
        response.render()
    return BeautifulSoup(response.content, "html.parser")


class ExtendedClient(Client):
    """Client with added features."""

    USER_IGNORE = -1

    def request(self, **request):
        """Request a response from the server."""
        response = super().request(**request)
        # Inspired by http://blog.borys.info/2012/12/django-testing-with-beautifulsoup.html
        response.soup = SimpleLazyObject(lambda: _get_soup(response))
        return response

    def force_login(self, user, backend=None):
        """
        Force given user to login.

        When `user` is `ExtendedClient.USER_IGNORE`, this method does nothing.
        When `user` is `None`, this will force a logout.
        In all other cases, `user` will be logged in.
        """
        if user == self.USER_IGNORE:
            return
        if user:
            super().force_login(user, backend)
        else:
            self.logout()

    def generic(self, *args, **kwargs):
        """
        Force given user to login, then fetch request and return response.

        This adds the optional keyword argument `user` to all methods that end up calling `generic`, including
        `get()` and `post()`.

        When no `user` is provided, or `user` is set to `ExtendedClient.USER_IGNORE`, no special action is taken.
        When `user` is `None`, the request will be performed on an anonymous request (user logged out).
        When `user` is provided and not `None`, the request will be performed with that user logged in.
        """
        self.force_login(kwargs.pop("user", self.USER_IGNORE))
        return super().generic(*args, **kwargs)
