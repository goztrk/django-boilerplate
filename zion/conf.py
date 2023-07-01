# Third Party (PyPI) Imports
from appconf import (
    AppConf,
)

# Django Imports
from django.conf import settings  # noqa


class ZionAppConf(AppConf):
    TEMPLATE_CONTEXT = "zion.views.contexts.template_context"
    SITE_NAME = "Zion"
    DEFAULT_HTTP_PROTOCOL = "http"

    class Meta:
        prefix = "zion"
