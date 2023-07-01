# Django Imports
from django.apps import (
    AppConfig,
)


class AccountConfig(AppConfig):
    name = "zion.apps.account"
    verbose_name = "Account"
    default_auto_field = "django.db.models.BigAutoField"
