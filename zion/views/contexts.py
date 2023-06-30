# Python Standard Library
from socket import (
    gethostname,
)


def template_context(request, context={}):
    context["server"] = {"hostname": gethostname()}
    return context
