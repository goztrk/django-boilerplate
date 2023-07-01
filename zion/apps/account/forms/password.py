# Django Imports
from django import forms
from django.utils.translation import gettext_lazy as _

# ZION Shared Library Imports
from zion.apps.account.hooks import hooks
from zion.apps.account.models import EmailAddress


class ChangePasswordForm(forms.Form):
    password_current = forms.CharField(
        label=_("Current Password"), widget=forms.PasswordInput(render_value=False)
    )
    password_new = forms.CharField(
        label=_("New Password"), widget=forms.PasswordInput(render_value=False)
    )
    password_new_confirm = forms.CharField(
        label=_("New Password (again)"), widget=forms.PasswordInput(render_value=False)
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password_current(self):
        if not self.user.check_password(self.cleaned_data.get("password_current")):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["password_current"]

    def clean_password_new_confirm(self):
        if (
            "password_new" in self.cleaned_data
            and "password_new_confirm" in self.cleaned_data
        ):
            password_new = self.cleaned_data["password_new"]
            password_new_confirm = self.cleaned_data["password_new_confirm"]
            return hooks.clean_password(password_new, password_new_confirm)
        return self.cleaned_data["password_new_confirm"]


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True)

    def clean_email(self):
        value = self.cleaned_data["email"]
        if not EmailAddress.objects.filter(email__iexact=value).exists():
            raise forms.ValidationError(_("Email address can not be found."))
        return value


class PasswordResetTokenForm(forms.Form):
    password = forms.CharField(
        label=_("New Password"), widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("New Password (again)"), widget=forms.PasswordInput(render_value=False)
    )

    def clean_password_confirm(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            password = self.cleaned_data["password"]
            password_confirm = self.cleaned_data["password_confirm"]
            return hooks.clean_password(password, password_confirm)
        return self.cleaned_data["password_confirm"]
