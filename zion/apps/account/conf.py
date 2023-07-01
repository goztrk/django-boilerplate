# Third Party (PyPI) Imports
from appconf import (
    AppConf,
)

# Django Imports
from django.conf import settings  # noqa


class AccountAppConf(AppConf):
    class Meta:
        prefix = "zion_account"
