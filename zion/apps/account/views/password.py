# Django Imports
from django.contrib import (
    auth,
    messages,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import (
    Http404,
    HttpResponseForbidden,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import (
    base36_to_int,
    int_to_base36,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView

# ZION Shared Library Imports
from zion.apps.account.conf import settings
from zion.apps.account.forms import (
    ChangePasswordForm,
    PasswordResetForm,
    PasswordResetTokenForm,
)
from zion.apps.account.hooks import hooks
from zion.apps.account.models import EmailAddress
from zion.apps.account.views.mixins import PasswordMixin


class ChangePasswordView(PasswordMixin, FormView):
    template_name = "account/password_change.html"
    form_class = ChangePasswordForm
    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": _("Password successfully changed."),
        }
    }
    form_password_field = "password_new"
    fallback_url_setting = "ZION_ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("account_password_reset")
        return super(ChangePasswordView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden()
        return super(ChangePasswordView, self).post(*args, **kwargs)

    def form_valid(self, form):
        self.change_password(form)
        self.create_password_history(form, self.request.user)
        self.after_change_password()
        return redirect(self.get_success_url())

    def get_user(self):
        return self.request.user

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {"user": self.request.user, "initial": self.get_initial()}
        if self.request.method in ["POST", "PUT"]:
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def change_password(self, form):
        user = super(ChangePasswordView, self).change_password(form)
        # required on Django >= 1.7 to keep the user authenticated
        if hasattr(auth, "update_session_auth_hash"):
            auth.update_session_auth_hash(self.request, user)


class PasswordResetView(FormView):
    template_name = "account/password_reset.html"
    template_name_sent = "account/password_reset_sent.html"
    form_class = PasswordResetForm
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PasswordResetView, self).get_context_data(**kwargs)
        if self.request.method == "POST" and "resend" in self.request.POST:
            context["resend"] = True
        return context

    def form_valid(self, form):
        self.send_email(form.cleaned_data["email"])
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_sent,
            "context": self.get_context_data(form=form),
        }
        return self.response_class(**response_kwargs)

    def send_email(self, email):
        User = get_user_model()
        protocol = settings.ZION_DEFAULT_HTTP_PROTOCOL
        current_site = get_current_site(self.request)
        email_qs = EmailAddress.objects.filter(email__iexact=email)
        for user in User.objects.filter(pk__in=email_qs.values("user")):
            uid = int_to_base36(user.id)
            token = self.make_token(user)
            password_reset_url = "{0}://{1}{2}".format(
                protocol,
                current_site.domain,
                reverse(
                    settings.ZION_ACCOUNT_PASSWORD_RESET_TOKEN_URL,
                    kwargs=dict(uidb36=uid, token=token),
                ),
            )
            ctx = {
                "user": user,
                "current_site": current_site,
                "password_reset_url": password_reset_url,
            }
            hooks.send_password_reset_email([email], ctx)

    def make_token(self, user):
        return self.token_generator.make_token(user)


INTERNAL_RESET_URL_TOKEN = "set-password"
INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


class PasswordResetTokenView(PasswordMixin, FormView):
    template_name = "account/password_reset_token.html"
    template_name_fail = "account/password_reset_token_fail.html"
    form_class = PasswordResetTokenForm
    token_generator = default_token_generator
    form_password_field = "password"
    fallback_url_setting = "ACCOUNT_PASSWORD_RESET_REDIRECT_URL"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        user = self.get_user()
        if user is not None:
            token = kwargs["token"]
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(
                    INTERNAL_RESET_SESSION_TOKEN, ""
                )
                if self.check_token(user, session_token):
                    return super(PasswordResetTokenView, self).dispatch(*args, **kwargs)
            else:
                if self.check_token(user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, INTERNAL_RESET_URL_TOKEN
                    )
                    return redirect(redirect_url)
        return self.token_fail()

    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ctx = self.get_context_data(form=form)
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = super(PasswordResetTokenView, self).get_context_data(**kwargs)
        ctx.update(
            {
                "uidb36": self.kwargs["uidb36"],
                "token": self.kwargs["token"],
            }
        )
        return ctx

    def form_valid(self, form):
        self.change_password(form)
        self.create_password_history(form, self.get_user())
        self.after_change_password()
        return redirect(self.get_success_url())

    def get_user(self):
        try:
            uid_int = base36_to_int(self.kwargs["uidb36"])
        except ValueError:
            raise Http404()
        return get_object_or_404(get_user_model(), id=uid_int)

    def check_token(self, user, token):
        return self.token_generator.check_token(user, token)

    def token_fail(self):
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_fail,
            "context": self.get_context_data(),
        }
        return self.response_class(**response_kwargs)
