from django.db import models, transaction
from django.core.exceptions import ValidationError

from accounting.models.mixins import IdentifiableMixin, TimestampedMixin
from accounting.models.journal_entry_detail import JournalEntryDetail


class JournalEntryManager(models.Manager):
    def create_from_details(self, *args, details=None, **kwargs):
        """
        Create a JournalEntry from a list of JournalEntryDetails

        Args:
        details: list - A list of unsaved JournalEntryDetails
        """
        if not isinstance(details, list):
            raise ValidationError(
                "Must provide a list of fields to create JournalEntryDetails"
            )

        credits = 0
        debits = 0
        for detail in details:
            if detail.normal == JournalEntryDetail.Normals.DEBIT:
                debits += detail.amount
            else:
                credits += detail.amount
        if credits != debits:
            raise ValidationError("Debits must equal Credits")

        with transaction.atomic():
            journal_entry = JournalEntry.objects.create(*args, **kwargs)
            for detail in details:
                detail.journal_entry = journal_entry
                detail.save()
        return journal_entry


class JournalEntry(IdentifiableMixin, TimestampedMixin, models.Model):
    """
    A collection of Credits and Debits for a transaction
    """

    # The effective date of the transaction
    date_effective = models.DateTimeField()

    objects = JournalEntryManager()
