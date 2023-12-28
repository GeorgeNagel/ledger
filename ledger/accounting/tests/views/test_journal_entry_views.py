import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from accounting.models.journal_entry import JournalEntry
from accounting.models.account_entry import AccountEntry
from accounting.tests.factories.account import AccountFactory
from accounting.tests.factories.journal_entry import JournalEntryFactory
from accounting.serializers.journal_entry import JournalEntrySerializer


class TestGetJournalEntry(TestCase):
    def test_get_returns_journal_entry(self):
        journal_entry = JournalEntryFactory()
        journal_entry_url = reverse("get_journal_entry", args=[journal_entry.id])

        response = self.client.get(journal_entry_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), JournalEntrySerializer(journal_entry).data)


class TestCreateJournalEntry(TestCase):
    def test_post_creates_new_journal_entry(self):
        account_1 = AccountFactory()
        account_2 = AccountFactory()
        self.assertFalse(JournalEntry.objects.exists())
        self.assertFalse(AccountEntry.objects.exists())
        journal_entry_url = reverse("create_journal_entry")
        request_data = {
            "account_entries": [
                {"account": account_1.id, "amount": 123, "normal": 1},
                {"account": account_2.id, "amount": 123, "normal": -1},
            ]
        }
        response = self.client.post(
            journal_entry_url, data=request_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JournalEntry.objects.count(), 1)
        journal_entry = JournalEntry.objects.first()
        self.assertEqual(response.json(), JournalEntrySerializer(journal_entry).data)
        self.assertEqual(AccountEntry.objects.count(), 2)
        account_entry_1 = AccountEntry.objects.get(
            journal_entry=journal_entry, account=account_1
        )
        self.assertEqual(account_entry_1.normal, AccountEntry.Normals.DEBIT)
        self.assertEqual(account_entry_1.amount, 123)
        account_entry_2 = AccountEntry.objects.get(
            journal_entry=journal_entry, account=account_2
        )
        self.assertEqual(account_entry_2.normal, AccountEntry.Normals.CREDIT)
        self.assertEqual(account_entry_2.amount, 123)
