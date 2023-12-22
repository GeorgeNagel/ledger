import factory

from accounting.models.account import Account


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounting.Account"

    balance = 0
    normal = Account.Normals.DEBIT
