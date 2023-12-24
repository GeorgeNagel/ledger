import factory

from accounting.models.account import Account
from accounting.tests.factories.account_holder import AccountHolderFactory


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounting.Account"

    balance = 0
    normal = Account.Normals.DEBIT
    account_holder = factory.SubFactory(AccountHolderFactory)
