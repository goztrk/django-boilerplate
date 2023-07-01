# Python Standard Library
from socket import gethostname

# ZION Shared Library Imports
from zion.conf import settings


def context_renderer(request, context={}):
    context["site_name"] = settings.ZION_SITE_NAME
    context["server"] = {"hostname": gethostname()}
    return context
