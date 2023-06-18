"""
Django Settings Environment Override
"""
# Application Imports
from core.settings.components.apps import (
    INSTALLED_APPS,
    )
from core.settings.components.middleware import (
    MIDDLEWARE,
    )
from core.settings.components.templates import (
    TEMPLATES,
    )


DEBUG = True
TEMPLATE_DEBUG = True

TEMPLATES[0]["OPTIONS"]["debug"] = TEMPLATE_DEBUG

INSTALLED_APPS += [
    "django_browser_reload",
]

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]
