# Python Standard Library
from typing import Any

# Django Imports
from django.contrib import auth
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView

# ZION Shared Library Imports
from zion.apps.account import signals
from zion.apps.account.conf import settings
from zion.apps.account.forms import (
    LoginEmailForm,
    LoginUsernameForm,
)
from zion.apps.account.utils import (
    default_redirect,
    get_form_data,
)
from zion.utils.http import is_ajax


@method_decorator(sensitive_post_parameters(), name="dispatch")
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class LoginView(FormView):
    template_name = "account/login.html"
    template_name_ajax = "account/ajax.login.html"
    form_class = LoginUsernameForm
    form_kwargs = {}
    redirect_field_name = "next"

    def __init__(self, **kwargs: Any) -> None:
        self.form_class = (
            LoginUsernameForm
            if settings.ZION_ACCOUNT_LOGIN_FIELD == "username"
            else LoginEmailForm
        )
        super().__init__(**kwargs)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(*args, **kwargs)

    def get_template_names(self):
        if is_ajax(self.request):
            return [self.template_name_ajax]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        context.update(
            {
                "redirect_field_name": redirect_field_name,
                "redirect_field_value": self.request.POST.get(
                    redirect_field_name, self.request.GET.get(redirect_field_name, "")
                ),
            }
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):
        signals.user_login_attempt.send(
            sender=LoginView,
            username=get_form_data(form, form.identifier_field),
            result=form.is_valid(),
        )
        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        self.login_user(form)
        self.after_login(form)
        return redirect(self.get_success_url())

    def after_login(self, form):
        signals.user_logged_in.send(sender=LoginView, user=form.user, form=form)

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.ZION_ACCOUNT_LOGIN_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def login_user(self, form):
        auth.login(self.request, form.user)
        expiry = (
            settings.ZION_ACCOUNT_REMEMBER_ME_EXPIRY
            if form.cleaned_data.get("remember")
            else 0
        )
        self.request.session.set_expiry(expiry)
