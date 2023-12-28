from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, F
from django.db.models.functions import Now

from accounting.models.mixins import IdentifiableMixin
from accounting.models.account_entry import AccountEntry


class StatementManager(models.Manager):
    def create(cls, *args, **kwargs):
        # Find the most recent statement before date_close, if any
        date_close = kwargs.get("date_close")
        account = kwargs.get("account")
        balance = kwargs.get("balance")
        previous_statement = (
            Statement.objects.filter(account=account, date_close__lt=date_close)
            .order_by("-date_close")
            .first()
        )

        # Validate AccountEntries since last Statement sum to expected balance
        account_entries_queryset = AccountEntry.objects.filter(
            account=account,
            created__lt=date_close,
        )
        if previous_statement:
            account_entries_queryset = account_entries_queryset.filter(
                created__gte=previous_statement.date_close
            )
        account_entries_sum = (
            account_entries_queryset.aggregate(sum=Sum(F("amount") * F("normal")))[
                "sum"
            ]
            or 0
        )

        if previous_statement:
            expected_balance_on_date_close = (
                previous_statement.balance + account_entries_sum
            )
        else:
            expected_balance_on_date_close = account_entries_sum

        if expected_balance_on_date_close != balance:
            raise ValidationError(
                "Statement balance must equal sum of previous statement balance and all AccountEntries until date close"
            )

        # Save Statement
        statement = Statement(**kwargs)
        statement.save()
        return statement


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

    objects = StatementManager()
