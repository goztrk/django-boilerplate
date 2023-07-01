# ZION Shared Library Imports
from zion.apps.account.conf import (
    settings,
)
from zion.utils.hooks import (
    ZionBaseHooks,
)


class AccountDefaultHooks(ZionBaseHooks):
    def generate_signup_code_token(self, email=None):
        return self.generate_random_token([email])


class HookProxy(object):
    def __getattr__(self, attr):
        return getattr(settings.ACCOUNT_HOOKS, attr)


hooks = HookProxy()
