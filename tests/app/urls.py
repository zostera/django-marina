from django.urls import path

from .views import HomeView, LoginRequiredView, SuperuserRequiredView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("authenticated/", LoginRequiredView.as_view(), name="access_authenticated"),
    path("superuser/", SuperuserRequiredView.as_view(), name="access_superuser"),
]
