"""
Django Settings Environment Override
"""
# Application Imports
from core.settings.components.apps import INSTALLED_APPS
from core.settings.components.templates import TEMPLATES


DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS = INSTALLED_APPS + ["django_browser_reload"]

TEMPLATES[0]["OPTIONS"]["debug"] = TEMPLATE_DEBUG
