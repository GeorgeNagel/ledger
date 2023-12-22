from django.db import models

from accounting.models.mixins import IdentifiableMixin, TimestampedMixin


class Account(IdentifiableMixin, TimestampedMixin, models.Model):
    class Normals(models.IntegerChoices):
        DEBIT = 1
        CREDIT = -1

    # Normal factor represents whether this is a debit-normal or credit-normal Account
    normal = models.IntegerField(choices=Normals)

    balance = models.IntegerField()
