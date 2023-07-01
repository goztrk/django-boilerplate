# Django Imports
from django.contrib import admin

# ZION Shared Library Imports
from zion.apps.account.models import (
    Account,
    EmailAddress,
)


# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


class EmailAddressAdmin(AccountAdmin):
    list_display = ["user", "email", "verified", "primary"]
    search_fields = ["email", "user__username"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


admin.site.register(Account, AccountAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
