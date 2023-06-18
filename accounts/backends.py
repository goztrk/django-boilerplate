"""
Accounts Backends
"""

# Python Standard Library
from typing import (
    Any,
    )

# Django Imports
from django.conf import (
    settings,
    )
from django.contrib.auth import (
    get_user_model,
    )
from django.contrib.auth.backends import (
    ModelBackend,
    )
from django.db.models import (
    Q,
    )
from django.http.request import (
    HttpRequest,
    )


UserModel = get_user_model()


class AccountsBackend(ModelBackend):
    """
    Accounts Backend
    """

    def authenticate(
        self,
        request: HttpRequest,
        username: str | None = ...,
        password: str | None = ...,
        **kwargs: Any
    ):
        if username is None or password is None:
            return

        try:
            query = None
            for field in settings.ACCOUNTS_LOGIN_WITH:
                query |= Q(**{field: username})
            user = UserModel.objects.get(query)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
