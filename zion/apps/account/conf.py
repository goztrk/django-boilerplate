# Third Party (PyPI) Imports
from appconf import (
    AppConf,
)

# Django Imports
from django.conf import settings  # noqa


class AccountAppConf(AppConf):
    CREATE_ON_SAVE = True
    EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
    EMAIL_CONFIRMATION_URL = "account:confirm_email"
    HOOKS = "zion.apps.account.hooks.AccountDefaultHooks"

    class Meta:
        prefix = "zion_account"
