from django.db import models, transaction
from django.db.models import F
from django.core.exceptions import ValidationError
from django.db.models.functions import Now

from accounting.models.account import Account
from accounting.models.mixins import IdentifiableMixin
from accounting.models.account_entry import AccountEntry


class JournalEntryManager(models.Manager):
    def create_from_account_entry_dicts(
        self, *args, account_entry_dicts=None, allow_negative_balances=True, **kwargs
    ):
        """
        Create a JournalEntry from a list of AccountEntries

        Args:
        account_entry_dicts: list - A list of AccountEntry dictionaries of the shape
            {
                "amount": <integer: cents>,
                "normal": <integer: +1/-1>,
                "account": <integer: Account id>
            }
        allow_negative_balances - When False, raises a ValidationError if the
            update would cause an account balance to go negative
        """
        if not isinstance(account_entry_dicts, list):
            raise ValidationError("Must provide a list of dictionaries")

        credits = 0
        debits = 0
        for account_entry_dict in account_entry_dicts:
            if account_entry_dict["normal"] == AccountEntry.Normals.DEBIT:
                debits += account_entry_dict["amount"]
            else:
                credits += account_entry_dict["amount"]
        if credits != debits:
            raise ValidationError("Debits must equal Credits")

        account_ids = [
            account_entry_dict["account"] for account_entry_dict in account_entry_dicts
        ]

        with transaction.atomic():
            journal_entry = JournalEntry.objects.create(*args, **kwargs)
            Account.objects.filter(id__in=account_ids).select_for_update()
            for account_entry_dict in account_entry_dicts:
                # Create the AccountEntry models
                account_entry = AccountEntry(
                    amount=account_entry_dict["amount"],
                    normal=account_entry_dict["normal"],
                    account_id=account_entry_dict["account"],
                )
                account_entry.journal_entry = journal_entry
                account_entry.save()

                # Update Account balances
                if allow_negative_balances:
                    # We can optimize the number of round-trip queries to Postgres
                    # by using atomic field updates if we don't care about potentially
                    # creating negative balances
                    Account.objects.filter(id=account_entry.account_id).update(
                        balance=F("balance")
                        + account_entry.amount * account_entry.normal * F("normal")
                    )
                else:
                    account_entry.account.balance += (
                        account_entry.account.normal
                        * account_entry.normal
                        * account_entry.amount
                    )
                    account_entry.account.save()
                    if (
                        account_entry.account.balance < 0
                        and not allow_negative_balances
                    ):
                        # This JournalEntry would result in a negative account balance, so
                        # unwind the atomic transaction
                        raise ValidationError(
                            "Negative account balances not allowed when allow_negative_balances flag is False"
                        )

        return journal_entry


class JournalEntry(IdentifiableMixin, models.Model):
    """
    A collection of Credits and Debits for a transaction
    """

    objects = JournalEntryManager()

    # Tracks when this record was inserted in the database
    # Note: when using Postgres, this should use
    # django.contrib.postgres.functions.TransactionNow instead
    # for consistent created timestamps within a db transaction
    created = models.DateTimeField(db_default=Now())
