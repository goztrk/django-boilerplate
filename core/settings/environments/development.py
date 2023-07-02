"""
Django Settings Environment Override
"""
# Python Standard Library
import os

# Application Imports
from core.settings.components.dirs import BASE_DIR
from core.settings.components.templates import TEMPLATES


DEBUG = True
TEMPLATE_DEBUG = True

TEMPLATES[0]["OPTIONS"]["debug"] = TEMPLATE_DEBUG

# To make static file serving work with `runserver`, `STATICFILES_DIRS` must be
# defined. But it does not work with `STATIC_ROOT`.
STATIC_ROOT = ""
STATICFILES_DIRS = [os.path.join(BASE_DIR.parent, "static")]
