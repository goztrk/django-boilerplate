# Django Imports
from django import forms
from django.utils.encoding import force_str


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", forms.PasswordInput(render_value=False))
        self.strip = kwargs.pop("strip", True)
        super(PasswordField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return ""
        value = force_str(value)
        if self.strip:
            value = value.strip()
        return value
