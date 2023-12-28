from django.db import models
from django.db.models.functions import Now

from accounting.models.mixins import IdentifiableMixin


class AccountHolder(IdentifiableMixin, models.Model):
    """
    An individual with access privileges to an account
    """

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    # Tracks when this record was inserted in the database
    # Note: when using Postgres, this should use
    # django.contrib.postgres.functions.TransactionNow instead
    # for consistent created timestamps within a db transaction
    created = models.DateTimeField(db_default=Now())

    # Tracks when this record was updated
    modified = models.DateTimeField(auto_now=True)
