# Third Party (PyPI) Imports
from appconf import AppConf

# Django Imports
from django.conf import settings  # noqa

# ZION Shared Library Imports
from zion.constants.timezones import TIMEZONES


class AccountAppConf(AppConf):
    LOGIN_FIELD = "username"
    CREATE_ON_SAVE = True
    LOGIN_URL = "account:login"
    LOGOUT_URL = "account:logout"
    SIGNUP_REDIRECT_URL = "/"
    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = "/"
    PASSWORD_STRIP = True
    REMEMBER_ME_EXPIRY = 60 * 60 * 24 * 365 * 10
    EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
    EMAIL_CONFIRMATION_AUTO_LOGIN = False
    EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "account:login"
    EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
    EMAIL_CONFIRMATION_URL = "account:confirm_email"
    HOOKS = "zion.apps.account.hooks.AccountDefaultHooks"
    TIMEZONES = TIMEZONES

    class Meta:
        prefix = "zion_account"
