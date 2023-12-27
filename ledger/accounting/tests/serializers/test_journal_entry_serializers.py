from django.test import TestCase

from accounting.tests.factories.journal_entry import JournalEntryFactory
from accounting.tests.factories.account import AccountFactory
from accounting.tests.factories.account_entry import AccountEntryFactory
from accounting.serializers.journal_entry import JournalEntrySerializer, CreateJournalEntrySerializer
from accounting.models.journal_entry import JournalEntry
from accounting.models.account_entry import AccountEntry


class TestJournalEntrySerializer(TestCase):
    def test_output_format(self):
        account_1 = AccountFactory()
        account_2 = AccountFactory()
        journal_entry = JournalEntryFactory()
        account_entry_1 = AccountEntryFactory(
            journal_entry=journal_entry,
            normal=AccountEntry.Normals.DEBIT,
            amount=123,
            account=account_1,
        )
        account_entry_2 = AccountEntryFactory(
            journal_entry=journal_entry,
            normal=AccountEntry.Normals.CREDIT,
            amount=123,
            account=account_2,
        )

        serializer = JournalEntrySerializer(journal_entry)

        output_format = serializer.data

        self.assertEqual(
            output_format,
            {
                "id": journal_entry.id,
                "uuid": str(journal_entry.uuid),
                "created": journal_entry.created.isoformat(),
                "account_entries": [
                    {
                        "id": account_entry_1.id,
                        "uuid": str(account_entry_1.uuid),
                        "created": account_entry_1.created.isoformat(),
                        "amount": 123,
                        "account": account_1.id,
                        "normal": 1,
                    },
                    {
                        "id": account_entry_2.id,
                        "uuid": str(account_entry_2.uuid),
                        "created": account_entry_2.created.isoformat(),
                        "amount": 123,
                        "account": account_2.id,
                        "normal": -1,
                    },
                ],
            },
        )

class TestCreateJournalEntrySerializer(TestCase):
    def test_save(self):
        self.assertEqual(JournalEntry.objects.count(), 0)
        self.assertEqual(AccountEntry.objects.count(), 0)
        account_1 = AccountFactory()
        account_2 = AccountFactory()
        data = {
            "account_entries": [
                {"account": account_1.id, "amount": 123, "normal": 1},
                {"account": account_2.id, "amount": 123, "normal": -1},
            ]
        }
        serializer = CreateJournalEntrySerializer(data=data)

        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        serializer.save()

        self.assertEqual(JournalEntry.objects.count(), 1)
        journal_entry = JournalEntry.objects.first()
        self.assertEqual(AccountEntry.objects.count(), 2)
        account_entry_1 = AccountEntry.objects.get(
            account=account_1, journal_entry=journal_entry
        )
        self.assertEqual(account_entry_1.normal, AccountEntry.Normals.DEBIT)
        self.assertEqual(account_entry_1.amount, 123)
        account_entry_2 = AccountEntry.objects.get(
            account=account_2, journal_entry=journal_entry
        )
        self.assertEqual(account_entry_2.normal, AccountEntry.Normals.CREDIT)
        self.assertEqual(account_entry_2.amount, 123)
