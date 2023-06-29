"""
Django Security Settings
"""

# Application Imports
from core.settings import (
    config,
)


SECRET_KEY = config("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [config("DOMAIN", default="localhost")]

CSRF_TRUSTED_ORIGINS = [config("DOMAIN_URL", default="http://localhost:8000")]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
