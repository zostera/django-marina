from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.utils.html import format_html
from django.views import View


class HomeView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("<html><head><title>Hi</title></head><body><h1 class='title'>Hi</h1></body></html>")


class LoginRequiredView(LoginRequiredMixin, HomeView):
    pass


class SuperuserRequiredView(PermissionRequiredMixin, HomeView):
    def has_permission(self):
        return self.request.user.is_superuser


class EchoView(View):
    def _response(self, data):
        return HttpResponse(format_html("<html><head><title>Echo</title></head><body>{data}</body></html>", data=data))

    def get(self, *args, **kwargs):
        return self._response(data=self.request.GET)

    def post(self, *args, **kwargs):
        return self._response(data=self.request.POST)
