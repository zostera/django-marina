from bs4 import BeautifulSoup


def remove_attrs(html, attrs=None):
    """Return html string without the specified tags."""
    if html and attrs:
        soup = BeautifulSoup(html, "html.parser")
        soup = _remove_attrs(soup, attrs)
        html = f"{soup}"
    return html


def _remove_attrs(soup, attrs):
    for attr in attrs:
        for tag in soup.find_all(attrs={attr: True}):
            del tag.attrs[attr]
    return soup
