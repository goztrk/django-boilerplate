# Django Imports
from django.db import (
    models,
)


class Account(models.Model):
    user = models.OneToOneField()
