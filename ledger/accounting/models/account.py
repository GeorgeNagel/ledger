from django.db import models
from django.db.models.functions import Now

from accounting.models.mixins import IdentifiableMixin
from accounting.models.utils import max_length_from_choices


class Account(IdentifiableMixin, models.Model):
    class Normals(models.IntegerChoices):
        DEBIT = 1
        CREDIT = -1

    class AccountTypes:
        SYSTEM = "system"
        CHECKING = "checking"
        LOANS_RECEIVABLE = "loans_receivable"
        CREDIT_CARD = "credit_card"
        DISCOUNT_ALLOWED = "discount_allowed"

    ACCOUNT_TYPE_CHOICES = {
        AccountTypes.SYSTEM: "System",
        AccountTypes.CHECKING: "Checking",
        AccountTypes.LOANS_RECEIVABLE: "Loans receivable",
        AccountTypes.CREDIT_CARD: "Credit card",
        AccountTypes.DISCOUNT_ALLOWED: "Discount allowed",
    }

    account_type = models.CharField(
        max_length=max_length_from_choices(ACCOUNT_TYPE_CHOICES),
        choices=ACCOUNT_TYPE_CHOICES,
        default=ACCOUNT_TYPE_CHOICES["checking"],
    )

    account_holder = models.ForeignKey(
        "accounting.AccountHolder", on_delete=models.DO_NOTHING
    )

    # Normal factor represents whether this is a debit-normal or credit-normal Account
    normal = models.IntegerField(choices=Normals)

    # The account balance, in cents
    balance = models.IntegerField(default=0)

    # Tracks when this record was inserted in the database
    # Note: when using Postgres, this should use
    # django.contrib.postgres.functions.TransactionNow instead
    # for consistent created timestamps within a db transaction
    created = models.DateTimeField(db_default=Now())

    # Tracks when this record was updated
    modified = models.DateTimeField(auto_now=True)
