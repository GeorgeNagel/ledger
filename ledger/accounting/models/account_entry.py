from django.db import models
from django.db.models.functions import Now
from django.core.validators import MinValueValidator

from accounting.models.mixins import IdentifiableMixin


class AccountEntry(IdentifiableMixin, models.Model):
    """
    Represents a single Debit or Credit of a JournalEntry
    """

    class Normals(models.IntegerChoices):
        DEBIT = 1
        CREDIT = -1

    # The JournalEntry to which this debit/credit belongs
    journal_entry = models.ForeignKey(
        "accounting.JournalEntry",
        on_delete=models.DO_NOTHING,
        related_name="account_entries",
    )

    # Account to which the debit/credit relates
    account = models.ForeignKey(
        "accounting.Account",
        on_delete=models.DO_NOTHING,
        related_name="account_entries",
    )

    # Tracks when this record was inserted in the database
    # Note: when using Postgres, this should use
    # django.contrib.postgres.functions.TransactionNow instead
    # for consistent created timestamps within a db transaction
    created = models.DateTimeField(db_default=Now())

    # The value of the debit/credit.
    # Amounts should always be positive.
    # Values are in cents.
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    # Normal factor represents whether this is a debit (+1 normal)
    # or credit (-1 normal)
    normal = models.IntegerField(choices=Normals)
