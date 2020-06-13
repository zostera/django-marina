from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    def get(self, request):
        return HttpResponse("<html><head><title>Hi</title></head><body><h1 class='title'>Hi</h1></body></html>")


class LoginRequiredView(LoginRequiredMixin, HomeView):
    pass


class SuperuserRequiredView(PermissionRequiredMixin, HomeView):
    def has_permission(self):
        return self.request.user.is_superuser
