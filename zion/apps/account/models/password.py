# Django Imports
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# ZION Shared Library Imports
from zion.apps.account.conf import settings


class PasswordHistory(models.Model):
    """
    Contains single password history for user.
    """

    class Meta:
        verbose_name = _("password history")
        verbose_name_plural = _("password histories")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="password_history",
        on_delete=models.CASCADE,
    )
    password = models.CharField(max_length=255)  # encrypted password
    timestamp = models.DateTimeField(default=timezone.now)  # password creation time


class PasswordExpiry(models.Model):
    """
    Holds the password expiration period for a single user.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="password_expiry",
        verbose_name=_("user"),
        on_delete=models.CASCADE,
    )
    expiry = models.PositiveIntegerField(default=0)
