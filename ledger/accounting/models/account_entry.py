from django.db import models
from django.core.validators import MinValueValidator

from accounting.models.mixins import IdentifiableMixin, TimestampedMixin


class AccountEntry(IdentifiableMixin, TimestampedMixin, models.Model):
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

    # The value of the debit/credit
    # Amounts should always be positive
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    # Normal factor represents whether this is a debit (+1 normal)
    # or credit (-1 normal)
    normal = models.IntegerField(choices=Normals)
