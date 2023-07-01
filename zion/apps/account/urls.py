# Django Imports
from django.urls import path

# ZION Shared Library Imports
from zion.apps.account import views


app_name = "account"
urlpatterns = [
    path(
        "confirm_email/<str:key>/",
        views.ConfirmEmailView.as_view(),
        name="confirm_email",
    )
]
