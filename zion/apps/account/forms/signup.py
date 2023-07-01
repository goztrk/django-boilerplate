# Django Imports
from django import forms
from django.utils.translation import gettext_lazy as _

# ZION Shared Library Imports
from zion.apps.account.conf import settings
from zion.apps.account.forms.constants import (
    ALL_NUM_RE,
    USER_FIELD_MAX_LENGTH,
    User,
)
from zion.apps.account.forms.fields import PasswordField
from zion.apps.account.models import EmailAddress
from zion.apps.account.utils import get_user_lookup_kwargs


class SignupForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        max_length=USER_FIELD_MAX_LENGTH,
        widget=forms.TextInput(),
        required=True,
    )
    email = forms.EmailField(label=_("Email"), widget=forms.TextInput(), required=True)
    password = PasswordField(
        label=_("Password"),
        strip=settings.ZION_ACCOUNT_PASSWORD_STRIP,
    )
    password_confirm = PasswordField(
        label=_("Password (again)"),
        strip=settings.ZION_ACCOUNT_PASSWORD_STRIP,
    )
    code = forms.CharField(max_length=64, required=False, widget=forms.HiddenInput())

    def clean_username(self):
        if not ALL_NUM_RE.search(self.cleaned_data["username"]):
            raise forms.ValidationError(
                _(
                    "Usernames can only contain letters, numbers and the following "
                    "special characters ./+/-/_"
                )
            )
        lookup_kwargs = get_user_lookup_kwargs(
            {"{username}__iexact": self.cleaned_data["username"]}
        )
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(
            _("This username is already taken. Please choose another.")
        )

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ZION_ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(
                    _("You must type the same password each time.")
                )
        return self.cleaned_data
