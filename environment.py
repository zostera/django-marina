import sys

try:
    import django

    django_version = django.get_version()
except Exception:
    django_version = "not available"

print(f"Python {sys.version.split()[0]} / Django {django_version}")
