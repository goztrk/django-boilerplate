# Django Imports
from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

# ZION Shared Library Imports
from zion.apps.account.conf import settings
from zion.utils.hooks import ZionBaseHooks


class AccountDefaultHooks(ZionBaseHooks):
    def send_invitation_email(self, to, ctx):
        subject = render_to_string("account/email/invite_user_subject.txt", ctx)
        message = render_to_string("account/email/invite_user.txt", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def send_confirmation_email(self, to, ctx):
        subject = render_to_string("account/email/email_confirmation_subject.txt", ctx)
        subject = "".join(subject.splitlines())  # remove superfluous line breaks
        message = render_to_string("account/email/email_confirmation_message.txt", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def send_password_change_email(self, to, ctx):
        subject = render_to_string("account/email/password_change_subject.txt", ctx)
        subject = "".join(subject.splitlines())
        message = render_to_string("account/email/password_change.txt", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def send_password_reset_email(self, to, ctx):
        subject = render_to_string("account/email/password_reset_subject.txt", ctx)
        subject = "".join(subject.splitlines())
        message = render_to_string("account/email/password_reset.txt", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def generate_signup_code_token(self, email=None):
        return self.generate_random_token([email])

    def generate_email_confirmation_token(self, email):
        return self.generate_random_token([email])

    def get_user_credentials(self, form, identifier_field):
        return {
            "username": form.cleaned_data[identifier_field],
            "password": form.cleaned_data["password"],
        }

    def clean_password(self, password_new, password_new_confirm):
        if password_new != password_new_confirm:
            raise forms.ValidationError(_("You must type the same password each time."))
        return password_new

    def account_delete_mark(self, deletion):
        deletion.user.is_active = False
        deletion.user.save()

    def account_delete_expunge(self, deletion):
        deletion.user.delete()


class HookProxy(object):
    def __getattr__(self, attr):
        return getattr(settings.ACCOUNT_HOOKS, attr)


hooks = HookProxy()
