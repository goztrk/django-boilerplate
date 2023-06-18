"""
Django App Settings
"""

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tailwind",
    "core",
    "accounts",
]

TAILWIND_APP_NAME = "core"

INTERNAL_IPS = [
    "127.0.0.1",
]
