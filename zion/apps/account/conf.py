# Third Party (PyPI) Imports
from appconf import AppConf

# Django Imports
from django.conf import settings  # noqa


class AccountAppConf(AppConf):
    CREATE_ON_SAVE = True
    LOGIN_URL = "account:login"
    LOGOUT_URL = "account:logout"
    SIGNUP_REDIRECT_URL = "/"
    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = "/"
    EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
    EMAIL_CONFIRMATION_AUTO_LOGIN = False
    EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "account:login"
    EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
    EMAIL_CONFIRMATION_URL = "account:confirm_email"
    HOOKS = "zion.apps.account.hooks.AccountDefaultHooks"

    class Meta:
        prefix = "zion_account"
