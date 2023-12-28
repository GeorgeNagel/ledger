from datetime import datetime, timedelta, timezone as py_timezone

from django.test import TestCase
from django.utils import timezone

from accounting.tests.factories.account import AccountFactory
from accounting.tests.factories.journal_entry import JournalEntryWithDebitAndCredit
from accounting.tests.factories.statement import StatementFactory
from accounting.serializers.statement import StatementSerializer
from accounting.models.statement import Statement


class TestStatementSerializer(TestCase):
    def test_output_format(self):
        account = AccountFactory()
        statement = StatementFactory(
            date_close=datetime(2000, 1, 1, tzinfo=py_timezone.utc),
            account=account,
            balance=0,
        )
        serializer = StatementSerializer(statement)

        output_format = serializer.data

        self.assertEqual(
            output_format,
            {
                "balance": 0,
                "created": statement.created.isoformat(),
                "date_close": "2000-01-01T00:00:00+00:00",
                "uuid": str(statement.uuid),
                "id": statement.id,
                "account": account.id,
            },
        )

    def test_save_creates_statement(self):
        self.assertEqual(Statement.objects.count(), 0)
        account = AccountFactory()
        transaction_date = timezone.now() - timedelta(days=1)
        statement_close_date = timezone.now()
        JournalEntryWithDebitAndCredit(
            debit__account=account, created=transaction_date, amount=123
        )

        data = {
            "account": account.id,
            "balance": 123,
            "date_close": statement_close_date.isoformat(),
        }
        serializer = StatementSerializer(data=data)

        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        serializer.save()

        self.assertEqual(Statement.objects.count(), 1)
        statement = Statement.objects.first()
        self.assertEqual(statement.balance, 123)
        self.assertEqual(statement.date_close, statement_close_date)
