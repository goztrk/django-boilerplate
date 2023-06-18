"""
Django Main Settings

Uses django-split-settings PyPI package
Default environment is `development`.
To change settings file set `DJANGO_ENV` in `.env` file
"""

# Third Party (PyPI) Imports
from decouple import config
from split_settings.tools import include, optional


ENV = config("DJANGO_ENV", default="development")

include(
    *[
        # Include all settings components
        "components/*.py",
        # Select the right environment
        f"environments/{ENV}.py",
        # Optionally override some settings
        optional("environment/local.py"),
    ]
)
