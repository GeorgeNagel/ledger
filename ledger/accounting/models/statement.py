from django.db import models
from django.utils import timezone

from accounting.models.mixins import IdentifiableMixin, TimestampedMixin


class Statement(IdentifiableMixin, TimestampedMixin, models.Model):
    """
    Ties out the balance of an account on a particular date
    """

    # The account for which this statement was prepared
    account = models.ForeignKey("accounting.Account", on_delete=models.DO_NOTHING)

    # The date on which the balance of the Account was tied out
    date_close = models.DateTimeField()

    # The balance of the Account on the close date
    balance = models.IntegerField()
