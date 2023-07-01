# Python Standard Library
from socket import (
    gethostname,
)

# ZION Shared Library Imports
from zion.utils import (
    zion_setting,
)


def template_context(request, context={}):
    context["site_name"] = zion_setting("ZION_SITE_NAME")
    context["server"] = {"hostname": gethostname()}
    return context
