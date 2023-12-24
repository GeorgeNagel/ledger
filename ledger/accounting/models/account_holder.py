from django.db import models

from accounting.models.mixins import IdentifiableMixin, TimestampedMixin


class AccountHolder(IdentifiableMixin, TimestampedMixin, models.Model):
    """
    An individual with access privileges to an account
    """

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
