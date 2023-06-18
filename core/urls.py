"""
URL configuration for core project.
"""
# Django Imports
from django.contrib import (
    admin,
    )
from django.urls import (
    include,
    path,
    )


urlpatterns = [
    path("admin/", admin.site.urls),

    path('accounts/', include('accounts.urls', namespace='accounts')),
]
