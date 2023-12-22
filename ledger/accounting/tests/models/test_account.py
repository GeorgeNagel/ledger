from datetime import datetime, timezone

from django.test import TestCase

from accounting.models.account import Account
from accounting.models.journal_entry import JournalEntry
from accounting.models.journal_entry_detail import JournalEntryDetail
from accounting.tests.factories.account import AccountFactory


class TestAccount(TestCase):
    def test_debit_journal_entries_increase_debit_normal_account_balance(self):
        account_one = AccountFactory(normal=Account.Normals.DEBIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        debit = JournalEntryDetail(
            account=account_one, normal=JournalEntryDetail.Normals.DEBIT, amount=50
        )
        credit = JournalEntryDetail(
            account=account_two, normal=JournalEntryDetail.Normals.CREDIT, amount=50
        )
        JournalEntry.objects.create_from_details(
            date_effective=datetime(2000, 1, 1, tzinfo=timezone.utc),
            details=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, 50)

    def test_debit_journal_entries_decrease_credit_normal_account_balance(self):
        account_one = AccountFactory(normal=Account.Normals.CREDIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        debit = JournalEntryDetail(
            account=account_one, normal=JournalEntryDetail.Normals.DEBIT, amount=50
        )
        credit = JournalEntryDetail(
            account=account_two, normal=JournalEntryDetail.Normals.CREDIT, amount=50
        )
        JournalEntry.objects.create_from_details(
            date_effective=datetime(2000, 1, 1, tzinfo=timezone.utc),
            details=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, -50)

    def test_credit_journal_entries_increase_credit_normal_account_balance(self):
        account_one = AccountFactory(normal=Account.Normals.CREDIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        debit = JournalEntryDetail(
            account=account_one, normal=JournalEntryDetail.Normals.CREDIT, amount=50
        )
        credit = JournalEntryDetail(
            account=account_two, normal=JournalEntryDetail.Normals.DEBIT, amount=50
        )
        JournalEntry.objects.create_from_details(
            date_effective=datetime(2000, 1, 1, tzinfo=timezone.utc),
            details=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, 50)

    def test_credit_journal_entries_decrease_debit_normal_account_balance(self):
        account_one = AccountFactory(normal=Account.Normals.DEBIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        debit = JournalEntryDetail(
            account=account_one, normal=JournalEntryDetail.Normals.CREDIT, amount=50
        )
        credit = JournalEntryDetail(
            account=account_two, normal=JournalEntryDetail.Normals.DEBIT, amount=50
        )
        JournalEntry.objects.create_from_details(
            date_effective=datetime(2000, 1, 1, tzinfo=timezone.utc),
            details=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, -50)
