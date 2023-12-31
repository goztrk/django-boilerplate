"""
Django Settings Environment Override
"""

# Application Imports
from core.settings.components.database import DATABASES


DEBUG = False

DATABASES["default"]["ATOMIC_REQUESTS"] = True

DJANGO_VITE_DEV_MODE = DEBUG
