# Python Standard Library
import datetime
from typing import (
    Collection,
)

# Django Imports
from django import (
    forms,
)
from django.contrib.sites.models import (
    Site,
)
from django.db import (
    models,
    transaction,
)
from django.urls import (
    reverse,
)
from django.utils import (
    timezone,
)

# ZION Shared Library Imports
from zion.apps.account import (
    signals,
)
from zion.apps.account.conf import (
    settings,
)
from zion.apps.account.hooks import (
    hooks,
)
from zion.apps.account.managers import (
    EmailAddressManager,
)


class EmailAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    verified = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)

    objects = EmailAddressManager()

    class Meta:
        app_label = "account"
        verbose_name = "Email Address"
        verbose_name_plural = "Email Addresses"
        unique_together = [("user", "email")]

    def __str__(self):
        return f"{self.email} ({self.user})"

    def set_as_primary(self, conditional=True):
        old_primary = EmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        self.user.email = self.email
        self.user.save()
        return True

    def send_confirmation(self, **kwargs):
        confirmation = EmailConfirmation.create(self)
        confirmation.send(**kwargs)
        return confirmation

    def change(self, new_email, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            self.user.email = new_email
            self.user.save()
            self.email = new_email
            self.verified = False
            self.save()
            if confirm:
                self.send_confirmation()

    def validate_unique(self, exclude: Collection[str] | None = ...) -> None:
        super().validate_unique(exclude)
        qs = EmailAddress.objects.filter(email__iexact=self.email)

        if qs.exists():
            raise forms.ValidationError(
                {"email": "A user is registered with this email address."}
            )


class EmailConfirmation(models.Model):
    email_address = models.ForeignKey(EmailAddress, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(null=True)
    key = models.CharField(max_length=64, unique=True)

    class Meta:
        app_label = "account"
        verbose_name = "Email Confirmation"

    def __str__(self):
        return f"confirmation for {self.email_address}"

    @classmethod
    def create(cls, email_address: EmailAddress):
        key = hooks.generate_email_confirmation_token(email_address.email)
        return cls._default_manager.create(email_address=email_address, key=key)

    @property
    def key_expired(self):
        expiration_date = self.sent_at + datetime.timedelta(
            days=settings.ZION_ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS
        )
        return expiration_date <= timezone.now()

    def confirm(self):
        if not self.key_expired and not self.email_address.verified:
            email_address = self.email_address
            email_address.verified = True
            email_address.set_as_primary(conditional=True)
            email_address.save()
            signals.email_confirmed.send(
                sender=self.__class__, email_address=email_address
            )
            return email_address

    def send(self, **kwargs):
        current_site = (
            kwargs["site"] if "site" in kwargs else Site.objects.get_current()
        )
        protocol = settings.ZION_DEFAULT_HTTP_PROTOCOL
        activate_url = "{0}://{1}{2}".format(
            protocol,
            current_site.domain,
            reverse(settings.ZION_ACCOUNT_EMAIL_CONFIRMATION_URL, args=[self.key]),
        )
        context = {
            "email_address": self.email_address,
            "user": self.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": self.key,
        }
        hooks.send_confirmation_email([self.email_address.email], context)
        self.sent_at = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(sender=self.__class__, confirmation=self)
