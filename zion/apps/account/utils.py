# Python Standard Library
import functools
from urllib.parse import urlparse

# Django Imports
from django.core.exceptions import SuspiciousOperation
from django.urls import (
    NoReverseMatch,
    reverse,
)


def default_redirect(request, fallback_url, **kwargs):
    redirect_field_name = kwargs.get("redirect_field_name", "next")
    next_url = request.POST.get(
        redirect_field_name, request.GET.get(redirect_field_name)
    )
    if not next_url:
        # try the session if available
        if hasattr(request, "session"):
            session_key_value = kwargs.get("session_key_value", "redirect_to")
            if session_key_value in request.session:
                next_url = request.session[session_key_value]
                del request.session[session_key_value]
    is_safe = functools.partial(
        ensure_safe_url,
        allowed_protocols=kwargs.get("allowed_protocols"),
        allowed_host=request.get_host(),
    )
    if next_url and is_safe(next_url):
        return next_url
    else:
        try:
            fallback_url = reverse(fallback_url)
        except NoReverseMatch:
            if callable(fallback_url):
                raise
            if "/" not in fallback_url and "." not in fallback_url:
                raise
        # assert the fallback URL is safe to return to caller. if it is
        # determined unsafe then raise an exception as the fallback value comes
        # from the a source the developer choose.
        is_safe(fallback_url, raise_on_fail=True)
        return fallback_url


def get_form_data(form, field_name, default=None):
    if form.prefix:
        key = "-".join([form.prefix, field_name])
    else:
        key = field_name
    return form.data.get(key, default)


def ensure_safe_url(
    url, allowed_protocols=None, allowed_host=None, raise_on_fail=False
):
    if allowed_protocols is None:
        allowed_protocols = ["http", "https"]
    parsed = urlparse(url)
    # perform security checks to ensure no malicious intent
    # (i.e., an XSS attack with a data URL)
    safe = True
    if parsed.scheme and parsed.scheme not in allowed_protocols:
        if raise_on_fail:
            raise SuspiciousOperation(
                "Unsafe redirect to URL with protocol '{0}'".format(parsed.scheme)
            )
        safe = False
    if allowed_host and parsed.netloc and parsed.netloc != allowed_host:
        if raise_on_fail:
            raise SuspiciousOperation(
                "Unsafe redirect to URL not matching host '{0}'".format(allowed_host)
            )
        safe = False
    return safe
