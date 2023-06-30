# Django Imports
from django.http import (
    HttpResponse,
)
from django.template import (
    loader,
)

# ZION Shared Library Imports
from zion.utils import (
    import_string,
    zion_setting,
)


def render(
    request, template_name, context=None, content_type=None, status=None, using=None
):
    """
    Return an HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    if context is not None and zion_setting("ZION_TEMPLATE_CONTEXT"):
        template_context_builder = import_string(zion_setting("ZION_TEMPLATE_CONTEXT"))
        data: dict = template_context_builder()
        data.update(context)
        context = data

    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
