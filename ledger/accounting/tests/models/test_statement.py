from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from accounting.tests.factories.account import AccountFactory
from accounting.tests.factories.statement import StatementFactory
from accounting.tests.factories.journal_entry import JournalEntryWithDebitAndCredit
from accounting.models.account_entry import AccountEntry
from accounting.models.statement import Statement


class TestStatement(TestCase):
    def test_save_with_no_transactions(self):
        account = AccountFactory()
        self.assertFalse(AccountEntry.objects.exists())
        self.assertFalse(Statement.objects.exists())
        date_close = timezone.now()

        Statement.objects.create(date_close=date_close, account=account, balance=0)

        self.assertTrue(Statement.objects.exists())

    def test_save_with_account_entries(self):
        account = AccountFactory()
        transaction_time = timezone.now() + timedelta(days=-1)
        statement_date_close = timezone.now()

        JournalEntryWithDebitAndCredit(
            amount=123, created=transaction_time, debit__account=account
        )

        Statement.objects.create(
            date_close=statement_date_close, account=account, balance=123
        )

        self.assertTrue(Statement.objects.exists())

    def test_save_fails_when_account_entries_dont_sum_to_balance(self):
        account = AccountFactory()
        transaction_time = timezone.now() + timedelta(days=-1)
        statement_date_close = timezone.now()

        JournalEntryWithDebitAndCredit(
            amount=123, created=transaction_time, debit__account=account
        )

        try:
            Statement.objects.create(
                date_close=statement_date_close, account=account, balance=100
            )
            self.fail(
                "Should not be able to create a Statement that doesn't match existing Account Entries"
            )
        except ValidationError:
            pass

        self.assertFalse(Statement.objects.exists())

    def test_save_with_account_entries_since_last_statement(self):
        account = AccountFactory()
        first_transaction_time = timezone.now() + timedelta(days=-3)
        previous_statement_close_date = timezone.now() + timedelta(days=-2)
        transaction_time = timezone.now() + timedelta(days=-1)
        statement_date_close = timezone.now()
        JournalEntryWithDebitAndCredit(
            amount=100, created=first_transaction_time, debit__account=account
        )
        StatementFactory(
            account=account, date_close=previous_statement_close_date, balance=100
        )
        JournalEntryWithDebitAndCredit(
            amount=123, created=transaction_time, debit__account=account
        )

        try:
            Statement.objects.create(
                date_close=statement_date_close, account=account, balance=223
            )
        except ValidationError:
            self.fail(
                "Should be able to create a Statement to close Account Entries since the last Statement"
            )

        self.assertEqual(Statement.objects.count(), 2)

    def test_save_between_existing_statements(self):
        account = AccountFactory()
        first_statement_close_date = timezone.now() + timedelta(days=-4)
        first_transaction_time = timezone.now() + timedelta(days=-3)
        third_statement_date_close = timezone.now() + timedelta(days=-2)
        second_transaction_time = timezone.now() + timedelta(days=-1)
        second_statement_date_close = timezone.now()
        StatementFactory(
            account=account, date_close=first_statement_close_date, balance=0
        )
        JournalEntryWithDebitAndCredit(
            amount=100, created=first_transaction_time, debit__account=account
        )
        JournalEntryWithDebitAndCredit(
            amount=10, created=second_transaction_time, debit__account=account
        )
        StatementFactory(
            account=account, date_close=second_statement_date_close, balance=110
        )

        try:
            Statement.objects.create(
                date_close=third_statement_date_close, account=account, balance=100
            )
        except ValidationError:
            self.fail(
                "Should be able to create a Statement to close Account Entries since the last Statement"
            )

        self.assertEqual(Statement.objects.count(), 3)
