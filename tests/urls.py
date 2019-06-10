from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse


def _response(request):
    lines = [f"method: {request.method}", f"user: {request.user}"]
    return HttpResponse("\n".join(lines))


def echo(request):
    return _response(request)


@login_required
def logged_in_only(request):
    return _response(request)


def superuser_only(request):
    if request.user.is_superuser:
        return _response(request)
    raise PermissionDenied()


urlpatterns = [
    url(r"^echo$", echo, name="echo"),
    url(r"^logged_in_only$", logged_in_only, name="logged_in_only"),
    url(r"^superuser_only$", superuser_only, name="superuser_only"),
]
