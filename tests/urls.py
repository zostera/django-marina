from django.conf.urls import url
from django.http import HttpResponse


def echo(request):
    lines = [f"method: {request.method}", f"user: {request.user}"]
    return HttpResponse("\n".join(lines))


urlpatterns = [url(r"^echo$", echo, name="echo")]
