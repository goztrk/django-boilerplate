# Django Imports
from django.urls import path

# ZION Shared Library Imports
from zion.apps.account import views


app_name = "account"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "confirm_email/<str:key>/",
        views.ConfirmEmailView.as_view(),
        name="confirm_email",
    ),
]
