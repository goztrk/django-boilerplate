# Django Imports
from django.db.models.signals import (
    post_save,
)
from django.dispatch import (
    Signal,
    receiver,
)

# ZION Shared Library Imports
from zion.apps.account.conf import (
    settings,
)
from zion.apps.account.models import (
    Account,
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, **kwargs):
    # Disable post_save during `manage.py loaddata``
    if kwargs.get("raw", False):
        return False

    user, created = kwargs["instance"], kwargs["created"]
    disabled = getattr(
        user, "_disable_account_creation", not settings.ZION_ACCOUNT_CREATE_ON_SAVE
    )
    if created and not disabled:
        Account.objects.create(user=user)


email_confirmed = Signal()
email_confirmation_sent = Signal()
