# Django Imports
from django.apps import (
    AppConfig,
)


# isort: off


class AccountConfig(AppConfig):
    name = "zion.apps.account"
    verbose_name = "Account"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        import zion.apps.account.signals  # noqa

        return super().ready()
