# Django Imports
from django.contrib import (
    auth,
    messages,
)
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import View

# ZION Shared Library Imports
from zion.apps.account.conf import settings
from zion.apps.account.models import EmailConfirmation
from zion.views.mixins import TemplateResponseMixin


class ConfirmEmailView(TemplateResponseMixin, View):
    http_method_names = ["get", "post"]
    messages = {
        "email_confirmed": {
            "level": messages.SUCCESS,
            "text": _("You have confirmed {email}."),
        },
        "email_confirmation_expired": {
            "level": messages.ERROR,
            "text": _("Email confirmation for {email} has expired."),
        },
    }

    template_name = {
        "get": "account/email_confirm.html",
        "post": "account/email_confirmed.html",
    }

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        self.user = self.request.user
        confirmed = confirmation.confirm() is not None
        if confirmed:
            self.after_confirmation(confirmation)
            if settings.EMAIL_CONFIRMATION_AUTO_LOGIN:
                self.user = self.login_user(confirmation.email_address.user)
            redirect_url = self.get_redirect_url()
            if not redirect_url:
                context = self.get_context_data()
                return self.render_to_response(context)
            if self.messages.get("email_confirmed"):
                messages.add_message(
                    self.request,
                    self.messages["email_confirmed"]["level"],
                    self.messages["email_confirmed"]["text"].format(
                        **{"email": confirmation.email_address.email}
                    ),
                )
        else:
            redirect_url = self.get_redirect_url()
            messages.add_message(
                self.request,
                self.messages["email_confirmation_expired"]["level"],
                self.messages["email_confirmation_expired"]["text"].format(
                    **{"email": confirmation.email_address.email}
                ),
            )
        return redirect(redirect_url)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except EmailConfirmation.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        qs = EmailConfirmation.objects.all()
        qs = qs.select_related("email_address__user")
        return qs

    def get_context_data(self, **kwargs):
        context = kwargs
        context["confirmation"] = self.object
        return context

    def after_confirmation(self, confirmation):
        user = confirmation.email_address.user
        user.is_active = True
        user.save()

    def login_user(self, user):
        user.backend = "django.contrib.auth.backend.ModelBackend"
        auth.login(self.request, user)
        return user

    def get_redirect_url(self):
        if self.user.is_authenticated:
            if not settings.ZION_ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL:
                return settings.ZION_ACCOUNT_LOGIN_REDIRECT_URL
            return settings.ZION_ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL
        else:
            return settings.ZION_ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL
