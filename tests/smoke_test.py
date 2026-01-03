"""
Minimal smoke test.

This test verifies that the package can be installed and that
its most basic public API is usable. It intentionally avoids
test frameworks and any optional dependencies.
"""


def main():
    import django

    import django_marina

    # Basic imports work
    assert django.get_version()
    assert hasattr(django_marina, "__version__")

    # One minimal functional call
    from django_marina.html import remove_attrs

    html = '<div class="x" data-test="y">Hello</div>'
    cleaned = remove_attrs(html, ["class"])
    assert 'class="x"' not in cleaned
    assert 'data-test="y"' in cleaned


if __name__ == "__main__":
    main()
