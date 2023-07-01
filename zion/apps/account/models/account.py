# Django Imports
from django.db import models

# ZION Shared Library Imports
from zion.apps.account.conf import settings
from zion.apps.account.models.email import EmailAddress
from zion.apps.account.models.fields import TimeZoneField


class Account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="account", on_delete=models.CASCADE
    )
    timezone = TimeZoneField()

    class Meta:
        app_label = "account"
        verbose_name = "Account"

    def __str__(self):
        return str(self.user)

    @classmethod
    def create(cls, request=None, **kwargs):
        create_email = kwargs.pop("create_email", True)
        confirm_email = kwargs.pop("confirm_email", None)

        account = cls(**kwargs)
        account.save()
        if create_email and account.user.email:
            kwargs = {"primary": True}
            if confirm_email is not None:
                kwargs["confirm"] = confirm_email
            EmailAddress.objects.add_email(account.user, account.user.email, **kwargs)
        return account
