from django.db import models

from accounting.models.mixins import IdentifiableMixin, TimestampedMixin


class JournalEntry(IdentifiableMixin, TimestampedMixin, models.Model):
    """
    A collection of Credits and Debits for a transaction
    """

    # The effective date of the transaction
    date_effective = models.DateTimeField()
