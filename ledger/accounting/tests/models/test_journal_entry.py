from datetime import datetime, timezone

from django.test import TestCase
from django.core.exceptions import ValidationError

from accounting.models.account import Account
from accounting.models.journal_entry_detail import JournalEntryDetail
from accounting.models.journal_entry import JournalEntry


class TestJournalEntry(TestCase):
    def test_credits_must_equal_debits(self):
        account_one = Account.objects.create(normal=Account.Normals.DEBIT)
        account_two = Account.objects.create(normal=Account.Normals.DEBIT)
        with self.assertRaisesRegex(ValidationError, "Debits must equal Credits"):
            debit = JournalEntryDetail(
                account=account_one, normal=JournalEntryDetail.Normals.DEBIT, amount=1
            )
            credit = JournalEntryDetail(
                account=account_two, normal=JournalEntryDetail.Normals.DEBIT, amount=2
            )
            JournalEntry.objects.create_from_details(
                date_effective=datetime(2000, 1, 1, tzinfo=timezone.utc),
                details=[debit, credit],
            )

    def test_supports_more_than_two_legs(self):
        # In some situations, it can be useful to create
        # a journal entry with credits/debits in more than two accounts
        account_one = Account.objects.create(normal=Account.Normals.DEBIT)
        account_two = Account.objects.create(normal=Account.Normals.DEBIT)
        account_three = Account.objects.create(normal=Account.Normals.CREDIT)

        debit_one = JournalEntryDetail(
            account=account_one, normal=JournalEntryDetail.Normals.DEBIT, amount=1
        )
        debit_two = JournalEntryDetail(
            account=account_two, normal=JournalEntryDetail.Normals.DEBIT, amount=1
        )
        credit = JournalEntryDetail(
            account=account_three, normal=JournalEntryDetail.Normals.CREDIT, amount=2
        )
        JournalEntry.objects.create_from_details(
            date_effective=datetime(2000, 1, 1, tzinfo=timezone.utc),
            details=[debit_one, debit_two, credit],
        )
        self.assertEqual(JournalEntryDetail.objects.count(), 3)
