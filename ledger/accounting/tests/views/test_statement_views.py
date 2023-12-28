from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from accounting.models.statement import Statement
from accounting.tests.factories.statement import StatementFactory
from accounting.tests.factories.journal_entry import JournalEntryWithDebitAndCredit
from accounting.tests.factories.account import AccountFactory
from accounting.serializers.statement import StatementSerializer


class TestGetStatement(TestCase):
    def test_get_returns_statement(self):
        statement = StatementFactory()
        statement_url = reverse("get_statement", args=[statement.id])

        response = self.client.get(statement_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), StatementSerializer(statement).data)


class TestListStatements(TestCase):
    def test_get_lists_statements(self):
        account = AccountFactory()
        statement_1 = StatementFactory(account=account, date_close=timezone.now() - timedelta(days=1))
        statement_2 = StatementFactory(account=account)
        list_statements_url = reverse("list_statements", args=[account.id])

        response = self.client.get(list_statements_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            StatementSerializer([statement_2, statement_1], many=True).data,
        )


class TestCreateStatement(TestCase):
    def test_post_creates_new_statement(self):
        account = AccountFactory()
        transaction_date = timezone.now() - timedelta(days=1)
        statement_close_data = timezone.now()
        JournalEntryWithDebitAndCredit(
            debit__account=account, amount=123, created=transaction_date
        )
        self.assertFalse(Statement.objects.exists())
        statement_url = reverse("create_statement")
        request_data = {
            "account": account.id,
            "balance": 123,
            "date_close": statement_close_data.isoformat(),
        }

        response = self.client.post(
            statement_url, data=request_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Statement.objects.count(), 1)
        statement = Statement.objects.first()
        self.assertEqual(response.json(), StatementSerializer(statement).data)
        self.assertEqual(statement.account, account)
        self.assertEqual(statement.balance, 123)
        self.assertEqual(statement.date_close, statement_close_data)
