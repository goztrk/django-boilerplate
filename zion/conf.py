# Third Party (PyPI) Imports
from appconf import (
    AppConf,
)

# Django Imports
from django.conf import settings  # noqa


class ZionAppConf(AppConf):
    TEMPLATE_CONTEXT = "zion.views.contexts.template_context"
    SITE_NAME = "Zion"

    class Meta:
        prefix = "zion"
