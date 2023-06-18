"""
URL configuration for core project.
"""
# Django Imports
from django.conf import (
    settings,
    )
from django.contrib import (
    admin,
    )
from django.urls import (
    include,
    path,
    )

# Application Imports
from core import (
    views,
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("test/", views.test),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
