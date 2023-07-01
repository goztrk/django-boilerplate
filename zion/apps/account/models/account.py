# Django Imports
from django.db import (
    models,
)

# ZION Shared Library Imports
from zion.apps.account.conf import (
    settings,
)


class Account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="account", on_delete=models.CASCADE
    )
