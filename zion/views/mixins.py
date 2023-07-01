# Django Imports
from django.core.exceptions import (
    ImproperlyConfigured,
)
from django.views.generic.base import (
    TemplateResponseMixin as DjangoTemplateResponseMixin,
)

# ZION Shared Library Imports
from zion.conf import (
    settings,
)
from zion.utils import (
    import_string,
)


class TemplateResponseMixin(DjangoTemplateResponseMixin):
    """A mixin that can be used to render a template"""

    @property
    def response_class(self):
        renderer = import_string(settings.ZION_TEMPLATE_CONTEXT)
        return renderer

    def get_template_names(self):
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'"
            )
        elif isinstance(self.template_name, dict):
            return [self.template_name[self.request.method]]
        else:
            return [self.template_name]
