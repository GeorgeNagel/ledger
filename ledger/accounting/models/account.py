from django.db import models
from django.db.models import Sum, F
from django.utils import timezone

from accounting.models.mixins import IdentifiableMixin, TimestampedMixin
from accounting.models.statement import Statement
from accounting.models.journal_entry_detail import JournalEntryDetail


class Account(IdentifiableMixin, TimestampedMixin, models.Model):
    class Normals(models.IntegerChoices):
        DEBIT = 1
        CREDIT = -1

    # Normal factor represents whether this is a debit-normal or credit-normal Account
    normal = models.IntegerField(choices=Normals)

    def get_balance(self):
        """
        Returns the balance of the account on a particular date
        Defaults to the current balance

        Returns:
        - Integer - The balance on the given date
        """

        # Get the balance from the most recent statement before the cutuoff, if any
        most_recent_statement = (
            Statement.objects.filter(account=self).order_by("-date_close").first()
        )
        if most_recent_statement:
            balance_as_of_last_statement = most_recent_statement.balance
            most_recent_statement_close_date = most_recent_statement.date_close
        else:
            balance_as_of_last_statement = 0
            most_recent_statement_close_date = None

        # Get any journal entries after the statement but before the cutoff, if any
        journal_entry_details_queryset = JournalEntryDetail.objects.filter(
            account_id=self.id
        )
        if most_recent_statement_close_date:
            journal_entry_details_queryset = journal_entry_details_queryset.filter(
                journal_entry__date_effective__gt=most_recent_statement_close_date,
            )
        journal_entry_detail_amounts_since_statement = (
            journal_entry_details_queryset.aggregate(
                normalized_sum=Sum(F("amount") * F("normal"))
            )["normalized_sum"]
        ) or 0

        journal_entry_detail_value_added_since_statement = (
            journal_entry_detail_amounts_since_statement * self.normal
        )
        current_balance = (
            balance_as_of_last_statement
            + journal_entry_detail_value_added_since_statement
        )
        return current_balance
