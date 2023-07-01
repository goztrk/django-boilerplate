# Python Standard Library
from collections import OrderedDict

# Django Imports
from django import forms
from django.contrib import auth
from django.utils.translation import gettext_lazy as _

# ZION Shared Library Imports
from zion.apps.account.conf import settings
from zion.apps.account.forms.constants import USER_FIELD_MAX_LENGTH
from zion.apps.account.forms.fields import PasswordField
from zion.apps.account.hooks import hooks


class LoginForm(forms.Form):
    password = PasswordField(
        label=_("Password"),
        strip=settings.ZION_ACCOUNT_PASSWORD_STRIP,
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False,
    )
    user = None
    identifier_field = "username"
    authentication_fail_message = _("Invalid credentials")

    def clean(self):
        if self._errors:
            return
        user = auth.authenticate(**self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is inactive"))
        else:
            raise forms.ValidationError(self.authentication_fail_message)
        return self.cleaned_data

    def user_credentials(self):
        return hooks.get_user_credentials(self, self.identifier_field)


class LoginUsernameForm(LoginForm):
    username = forms.CharField(
        label=_("Username"),
        max_length=USER_FIELD_MAX_LENGTH,
    )
    authentication_fail_message = _(
        "The username and/or password you specified are not correct."
    )
    identifier_field = "username"

    def __init__(self, *args, **kwargs):
        super(LoginUsernameForm, self).__init__(*args, **kwargs)
        field_order = ["username", "password", "remember"]
        if hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)


class LoginEmailForm(LoginForm):
    email = forms.EmailField(label=_("Email"))
    authentication_fail_message = _(
        "The email address and/or password you specified are not correct."
    )
    identifier_field = "email"

    def __init__(self, *args, **kwargs):
        super(LoginEmailForm, self).__init__(*args, **kwargs)
        field_order = ["email", "password", "remember"]
        if hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)
