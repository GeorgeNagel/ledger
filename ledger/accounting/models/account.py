from django.db import models

from accounting.models.mixins import IdentifiableMixin, TimestampedMixin
from accounting.models.utils import max_length_from_choices


class Account(IdentifiableMixin, TimestampedMixin, models.Model):
    class Normals(models.IntegerChoices):
        DEBIT = 1
        CREDIT = -1

    ACCOUNT_TYPE_CHOICES = {
        "system": "System",
        "checking": "Checking",
        "loans_receivable": "Loans receivable",
        "credit_card": "Credit card",
        "discount_allowed": "Discount allowed",
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

    balance = models.IntegerField()
