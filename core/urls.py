"""
URL configuration for core project.
"""
# Django Imports
from django.contrib import admin
from django.urls import (
    include,
    path,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("zion.apps.account.urls", namespace="account")),
]
