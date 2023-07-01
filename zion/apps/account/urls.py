# Django Imports
from django.urls import path

# ZION Shared Library Imports
from zion.apps.account import views


app_name = "account"
urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "confirm_email/<str:key>/",
        views.ConfirmEmailView.as_view(),
        name="confirm_email",
    ),
    path("password/", views.ChangePasswordView.as_view(), name="password"),
    path("password/reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/<str:uidb36>/<str:token>/",
        views.PasswordResetTokenView.as_view(),
        name="password_reset_token",
    ),
    path("settings/", views.SettingsView.as_view(), name="settings"),
]
