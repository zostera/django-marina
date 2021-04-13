from django.urls import path

from .views import EchoView, HomeView, LoginRequiredView, MessageView, SuperuserRequiredView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("authenticated/", LoginRequiredView.as_view(), name="access_authenticated"),
    path("superuser/", SuperuserRequiredView.as_view(), name="access_superuser"),
    path("echo/", EchoView.as_view(), name="echo"),
    path("message/", MessageView.as_view(), name="message"),
]
