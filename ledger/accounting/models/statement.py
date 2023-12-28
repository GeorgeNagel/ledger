from django.db import models
from django.db.models.functions import Now

from accounting.models.mixins import IdentifiableMixin


class Statement(IdentifiableMixin, models.Model):
    """
    Ties out the balance of an account on a particular date
    """

    # The account for which this statement was prepared
    account = models.ForeignKey("accounting.Account", on_delete=models.DO_NOTHING)

    # The date on which the balance of the Account was tied out
    date_close = models.DateTimeField()

    # The balance of the Account on the close date
    balance = models.IntegerField()

    # Tracks when this record was inserted in the database
    # Note: when using Postgres, this should use
    # django.contrib.postgres.functions.TransactionNow instead
    # for consistent created timestamps within a db transaction
    created = models.DateTimeField(db_default=Now())
