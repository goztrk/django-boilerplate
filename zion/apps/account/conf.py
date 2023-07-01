# Third Party (PyPI) Imports
from appconf import AppConf

# Django Imports
from django.conf import settings  # noqa

# ZION Shared Library Imports
from zion.constants.languages import LANGUAGES
from zion.constants.timezones import TIMEZONES


class AccountAppConf(AppConf):
    OPEN_SIGNUP = True
    CREATE_ON_SAVE = True

    USER_DISPLAY = lambda user: user.username  # noqa

    LOGIN_FIELD = "username"
    REMEMBER_ME_EXPIRY = 60 * 60 * 24 * 365 * 10

    LOGIN_URL = "account:login"
    LOGOUT_URL = "account:logout"
    SIGNUP_REDIRECT_URL = "/"
    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = "/"
    SETTINGS_REDIRECT_URL = "account:settings"
    PASSWORD_CHANGE_REDIRECT_URL = "account:password"
    PASSWORD_RESET_REDIRECT_URL = "account:login"
    PASSWORD_RESET_TOKEN_URL = "account:password_reset_token"
    EMAIL_CONFIRMATION_URL = "account:confirm_email"
    EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "account:login"
    EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None

    PASSWORD_EXPIRY = 0
    PASSWORD_USE_HISTORY = False
    PASSWORD_STRIP = True
    NOTIFY_ON_PASSWORD_CHANGE = True

    EMAIL_UNIQUE = True
    EMAIL_CONFIRMATION_REQUIRED = False
    EMAIL_CONFIRMATION_EMAIL = True
    EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
    EMAIL_CONFIRMATION_AUTO_LOGIN = False

    DELETION_EXPUNGE_HOURS = 48

    HOOKS = "zion.apps.account.hooks.AccountDefaultHooks"
    TIMEZONES = TIMEZONES
    LANGUAGES = LANGUAGES

    class Meta:
        prefix = "zion_account"
