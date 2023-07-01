# Third Party (PyPI) Imports
from appconf import AppConf

# Django Imports
from django.conf import settings  # noqa


class ZionAppConf(AppConf):
    CONTEXT_RENDERER = "zion.utils.views.context_renderer"
    SITE_NAME = "Zion"
    DEFAULT_HTTP_PROTOCOL = "http"

    class Meta:
        prefix = "zion"
