# Django Imports
from django import forms
from django.utils.translation import gettext_lazy as _

# ZION Shared Library Imports
from zion.apps.account.conf import settings
from zion.apps.account.models import EmailAddress


class SettingsForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True)
    timezone = forms.ChoiceField(
        label=_("Timezone"),
        choices=[("", "---------")] + settings.ZION_ACCOUNT_TIMEZONES,
        required=False,
    )
    if settings.USE_I18N:
        language = forms.ChoiceField(
            label=_("Language"), choices=settings.ZION_ACCOUNT_LANGUAGES, required=False
        )

    def clean_email(self):
        value = self.cleaned_data["email"]
        if self.initial.get("email") == value:
            return value
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ZION_ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))
