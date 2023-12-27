from django.test import TestCase
from django.core.exceptions import ValidationError

from accounting.models.account import Account
from accounting.models.account_entry import AccountEntry
from accounting.models.journal_entry import JournalEntry

from accounting.tests.factories.account import AccountFactory


class TestJournalEntryManager(TestCase):
    def test_credits_must_equal_debits(self):
        account_one = AccountFactory(normal=Account.Normals.DEBIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        with self.assertRaisesRegex(ValidationError, "Debits must equal Credits"):
            debit = {"account": account_one.id, "normal": 1, "amount": 1}
            credit = {"account": account_two.id, "normal": -1, "amount": 2}
            JournalEntry.objects.create_from_account_entry_dicts(
                account_entry_dicts=[debit, credit],
            )

    def test_supports_more_than_two_legs(self):
        # In some situations, it can be useful to create
        # a journal entry with credits/debits in more than two accounts
        account_one = AccountFactory(normal=Account.Normals.DEBIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        account_three = AccountFactory(normal=Account.Normals.CREDIT)

        debit_one = {"account": account_one.id, "normal": 1, "amount": 1}
        debit_two = {"account": account_two.id, "normal": 1, "amount": 1}
        credit = {"account": account_three.id, "normal": -1, "amount": 2}
        JournalEntry.objects.create_from_account_entry_dicts(
            account_entry_dicts=[debit_one, debit_two, credit],
        )
        self.assertEqual(AccountEntry.objects.count(), 3)

    def test_supports_flag_for_no_negative_balances(self):
        account_one = AccountFactory(normal=Account.Normals.DEBIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)

        debit = {"account": account_one.id, "normal": 1, "amount": 1}
        # This credit would cause account_two to have a negative balance
        credit = {"account": account_two.id, "normal": -1, "amount": 1}
        try:
            JournalEntry.objects.create_from_account_entry_dicts(
                account_entry_dicts=[debit, credit],
                allow_negative_balances=False,
            )
            self.fail(
                "Should not allow negative balances when passing in the allow_negative_balances=False flag"
            )
        except ValidationError:
            pass

        self.assertEqual(AccountEntry.objects.count(), 0)
        account_one.refresh_from_db()
        account_two.refresh_from_db()
        self.assertEqual(account_one.balance, 0)
        self.assertEqual(account_two.balance, 0)

    def test_debit_journal_entries_increase_debit_normal_account_balance(self):
        account_one = AccountFactory(normal=Account.Normals.DEBIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        debit = {"account": account_one.id, "normal": 1, "amount": 50}
        credit = {"account": account_two.id, "normal": -1, "amount": 50}
        JournalEntry.objects.create_from_account_entry_dicts(
            account_entry_dicts=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, 50)

    def test_debit_journal_entries_decrease_credit_normal_account_balance(self):
        account_one = AccountFactory(normal=Account.Normals.CREDIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        debit = {"account": account_one.id, "normal": 1, "amount": 50}
        credit = {"account": account_two.id, "normal": -1, "amount": 50}
        JournalEntry.objects.create_from_account_entry_dicts(
            account_entry_dicts=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, -50)

    def test_credit_journal_entries_increase_credit_normal_account_balance(self):
        account_one = AccountFactory(normal=Account.Normals.CREDIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        debit = {"account": account_one.id, "normal": -1, "amount": 50}
        credit = {"account": account_two.id, "normal": 1, "amount": 50}
        JournalEntry.objects.create_from_account_entry_dicts(
            account_entry_dicts=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, 50)

    def test_credit_journal_entries_decrease_debit_normal_account_balance(self):
        account_one = AccountFactory(normal=Account.Normals.DEBIT)
        account_two = AccountFactory(normal=Account.Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        debit = {"account": account_one.id, "normal": -1, "amount": 50}
        credit = {"account": account_two.id, "normal": 1, "amount": 50}
        JournalEntry.objects.create_from_account_entry_dicts(
            account_entry_dicts=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, -50)
