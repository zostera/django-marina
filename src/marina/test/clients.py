from django.test import Client


class ClientWithFetch(Client):
    """
    Client that implements a shortcut `fetch`
    """

    def fetch(self, url, user, method="GET", **kwargs):
        """
        Login user or logout if user is None, fetch response for url and return it.

        :param url: Url to fetch
        :param user: User to login (None for logout)
        :param method: GET or POST
        :param kwargs: kwargs for fetching response
        :return: HttpResponse
        """
        self.logout()
        if user:
            self.force_login(user)
        if method == "GET":
            response = self.get(url, **kwargs)
        elif method == "POST":
            response = self.post(url, **kwargs)
        else:
            raise ValueError(f"Method should be GET or POST, not '{method}'.")
        return response
