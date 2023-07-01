"""
Django Path Settings
"""

# Python Standard Library
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

ROOT_URLCONF = "core.urls"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

WSGI_APPLICATION = "core.wsgi.application"
