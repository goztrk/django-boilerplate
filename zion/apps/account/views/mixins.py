# Django Imports
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _

# ZION Shared Library Imports
from zion.apps.account import signals
from zion.apps.account.conf import settings
from zion.apps.account.hooks import hooks
from zion.apps.account.models import PasswordHistory
from zion.apps.account.utils import default_redirect


class PasswordMixin(object):
    """
    Mixin handling common elements of password change.

    Required attributes in inheriting class:

      form_password_field - example: "password"
      fallback_url_setting - example: "ACCOUNT_PASSWORD_RESET_REDIRECT_URL"

    Required methods in inheriting class:

      get_user()
      change_password()
      after_change_password()
      get_redirect_field_name()

    """

    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": _("Password successfully changed."),
        }
    }

    def get_context_data(self, **kwargs):
        ctx = super(PasswordMixin, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update(
            {
                "redirect_field_name": redirect_field_name,
                "redirect_field_value": self.request.POST.get(
                    redirect_field_name, self.request.GET.get(redirect_field_name, "")
                ),
            }
        )
        return ctx

    def change_password(self, form):
        user = self.get_user()
        user.set_password(form.cleaned_data[self.form_password_field])
        user.save()
        return user

    def after_change_password(self):
        user = self.get_user()
        signals.password_changed.send(sender=self, user=user)
        if settings.ZION_ACCOUNT_NOTIFY_ON_PASSWORD_CHANGE:
            self.send_password_email(user)
        if self.messages.get("password_changed"):
            messages.add_message(
                self.request,
                self.messages["password_changed"]["level"],
                self.messages["password_changed"]["text"],
            )

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = getattr(settings, self.fallback_url_setting, None)
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def send_password_email(self, user):
        protocol = settings.ZION_DEFAULT_HTTP_PROTOCOL
        current_site = get_current_site(self.request)
        ctx = {
            "user": user,
            "protocol": protocol,
            "current_site": current_site,
        }
        hooks.send_password_change_email([user.email], ctx)

    def create_password_history(self, form, user):
        if settings.ZION_ACCOUNT_PASSWORD_USE_HISTORY:
            password = form.cleaned_data[self.form_password_field]
            PasswordHistory.objects.create(user=user, password=make_password(password))
