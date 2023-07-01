# ZION Shared Library Imports
from zion.apps.account.conf import settings
from zion.utils.hooks import ZionBaseHooks


class AccountDefaultHooks(ZionBaseHooks):
    def generate_signup_code_token(self, email=None):
        return self.generate_random_token([email])

    def get_user_credentials(self, form, identifier_field):
        return {
            "username": form.cleaned_data[identifier_field],
            "password": form.cleaned_data["password"],
        }


class HookProxy(object):
    def __getattr__(self, attr):
        return getattr(settings.ACCOUNT_HOOKS, attr)


hooks = HookProxy()
