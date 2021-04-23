from django.urls import path

from .views import EchoView, HomeView, LoginRequiredView, LoginView, MessageView, SuperuserRequiredView, redirect_root

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("authenticated/", LoginRequiredView.as_view(), name="access_authenticated"),
    path("superuser/", SuperuserRequiredView.as_view(), name="access_superuser"),
    path("echo/", EchoView.as_view(), name="echo"),
    path("message/", MessageView.as_view(), name="message"),
    path("redirect-root/", redirect_root, name="redirect-root"),
]
