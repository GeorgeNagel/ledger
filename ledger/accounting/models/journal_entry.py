from django.db import models, transaction
from django.core.exceptions import ValidationError

from accounting.models.account import Account
from accounting.models.mixins import IdentifiableMixin, TimestampedMixin
from accounting.models.journal_entry_detail import JournalEntryDetail


class JournalEntryManager(models.Manager):
    def create_from_details(
        self, *args, details=None, allow_negative_balances=True, **kwargs
    ):
        """
        Create a JournalEntry from a list of JournalEntryDetails

        Args:
        details: list - A list of unsaved JournalEntryDetails
        allow_negative_balances - When False, raises a ValidationError if the
            update would cause an account balance to go negative
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

        account_ids = [detail.account.id for detail in details]

        with transaction.atomic():
            journal_entry = JournalEntry.objects.create(*args, **kwargs)
            Account.objects.filter(id__in=account_ids).select_for_update()
            for detail in details:
                detail.journal_entry = journal_entry
                detail.save()
                detail.account.balance += (
                    detail.account.normal * detail.normal * detail.amount
                )
                detail.account.save()
                if detail.account.balance < 0 and not allow_negative_balances:
                    # This JournalEntry would result in a negative account balance, so
                    # unwind the atomic transaction
                    raise ValidationError(
                        "Negative account balances not allowed when allow_negative_balances flag is False"
                    )

        return journal_entry


class JournalEntry(IdentifiableMixin, TimestampedMixin, models.Model):
    """
    A collection of Credits and Debits for a transaction
    """

    # The effective date of the transaction
    effective_date = models.DateTimeField()

    objects = JournalEntryManager()
