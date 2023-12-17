from datetime import datetime, timezone as py_timezone

from django.test import TestCase
from django.utils import timezone

from accounting.models.account import Account
from accounting.models.statement import Statement
from accounting.models.journal_entry import JournalEntry
from accounting.models.journal_entry_detail import JournalEntryDetail


class TestGetAccountBalance(TestCase):
    def test_zero_for_account_with_no_journal_entries_or_statements(self):
        account = Account.objects.create(normal=Account.Normals.DEBIT)
        balance = account.get_balance()
        self.assertEqual(balance, 0)

    def test_statement_no_journal_entries(self):
        account = Account.objects.create(normal=Account.Normals.DEBIT)
        Statement.objects.create(
            account=account, date_close=timezone.now(), balance=123
        )
        balance = account.get_balance()
        self.assertEqual(balance, 123)

    def test_journal_entries_no_statement(self):
        account = Account.objects.create(normal=Account.Normals.DEBIT)
        journal_entry = JournalEntry.objects.create(date_effective=timezone.now())
        JournalEntryDetail.objects.create(
            account=account,
            journal_entry=journal_entry,
            amount=123,
            normal=JournalEntryDetail.Normals.DEBIT,
        )
        balance = account.get_balance()
        self.assertEqual(balance, 123)

    def test_journal_entries_since_statement(self):
        account = Account.objects.create(normal=Account.Normals.DEBIT)
        Statement.objects.create(
            account=account, date_close=timezone.now(), balance=100
        )
        journal_entry = JournalEntry.objects.create(date_effective=timezone.now())
        JournalEntryDetail.objects.create(
            account=account,
            journal_entry=journal_entry,
            amount=50,
            normal=JournalEntryDetail.Normals.DEBIT,
        )
        balance = account.get_balance()
        self.assertEqual(balance, 150)

    def test_multiple_statements(self):
        account = Account.objects.create(normal=Account.Normals.DEBIT)
        Statement.objects.create(
            account=account,
            date_close=datetime(2000, 1, 1, tzinfo=py_timezone.utc),
            balance=100,
        )
        first_journal_entry = JournalEntry.objects.create(
            date_effective=datetime(200, 1, 2, tzinfo=py_timezone.utc)
        )
        JournalEntryDetail.objects.create(
            account=account,
            journal_entry=first_journal_entry,
            amount=50,
            normal=JournalEntryDetail.Normals.DEBIT,
        )

        second_journal_entry = JournalEntry.objects.create(
            date_effective=datetime(2000, 1, 3, tzinfo=py_timezone.utc)
        )
        JournalEntryDetail.objects.create(
            account=account,
            journal_entry=second_journal_entry,
            amount=60,
            normal=JournalEntryDetail.Normals.DEBIT,
        )

        Statement.objects.create(
            account=account,
            date_close=datetime(2000, 2, 1, tzinfo=py_timezone.utc),
            balance=200,
        )
        third_journal_entry = JournalEntry.objects.create(
            date_effective=datetime(2000, 2, 2, tzinfo=py_timezone.utc)
        )
        JournalEntryDetail.objects.create(
            account=account,
            journal_entry=third_journal_entry,
            amount=70,
            normal=JournalEntryDetail.Normals.DEBIT,
        )
        balance = account.get_balance()
        self.assertEqual(balance, 270)

    def test_debit_journal_entries_increase_debit_normal_account_balance(self):
        account = Account.objects.create(normal=Account.Normals.DEBIT)
        journal_entry = JournalEntry.objects.create(date_effective=timezone.now())
        JournalEntryDetail.objects.create(
            account=account,
            journal_entry=journal_entry,
            amount=50,
            normal=JournalEntryDetail.Normals.DEBIT,
        )
        balance = account.get_balance()
        self.assertEqual(balance, 50)

    def test_debit_journal_entries_decrease_credit_normal_account_balance(self):
        account = Account.objects.create(normal=Account.Normals.CREDIT)
        journal_entry = JournalEntry.objects.create(date_effective=timezone.now())
        JournalEntryDetail.objects.create(
            account=account,
            journal_entry=journal_entry,
            amount=50,
            normal=JournalEntryDetail.Normals.DEBIT,
        )
        balance = account.get_balance()
        self.assertEqual(balance, -50)

    def test_credit_journal_entries_increase_credit_normal_account_balance(self):
        account = Account.objects.create(normal=Account.Normals.CREDIT)
        journal_entry = JournalEntry.objects.create(date_effective=timezone.now())
        JournalEntryDetail.objects.create(
            account=account,
            journal_entry=journal_entry,
            amount=50,
            normal=JournalEntryDetail.Normals.CREDIT,
        )
        balance = account.get_balance()
        self.assertEqual(balance, 50)

    def test_credit_journal_entries_decrease_debit_normal_account_balance(self):
        account = Account.objects.create(normal=Account.Normals.DEBIT)
        journal_entry = JournalEntry.objects.create(date_effective=timezone.now())
        JournalEntryDetail.objects.create(
            account=account,
            journal_entry=journal_entry,
            amount=50,
            normal=JournalEntryDetail.Normals.CREDIT,
        )
        balance = account.get_balance()
        self.assertEqual(balance, -50)
