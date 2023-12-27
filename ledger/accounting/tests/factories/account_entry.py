import factory

from accounting.models.account_entry import AccountEntry
from accounting.tests.factories.account import AccountFactory
from accounting.tests.factories.journal_entry import JournalEntryFactory


class AccountEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounting.AccountEntry"

    amount = 0
    normal = AccountEntry.Normals.DEBIT
    account = factory.SubFactory(AccountFactory)
    journal_entry = factory.SubFactory(JournalEntryFactory)
