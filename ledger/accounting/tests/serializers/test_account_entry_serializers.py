from django.test import TestCase

from accounting.tests.factories.account_entry import AccountEntryFactory
from accounting.serializers.account_entry import AccountEntrySerializer
from accounting.models.account_entry import AccountEntry


class TestAccountEntrySerializer(TestCase):
    def test_output_format(self):
        account_entry = AccountEntryFactory(
            normal=AccountEntry.Normals.DEBIT, amount=123
        )
        serializer = AccountEntrySerializer(account_entry)

        output_format = serializer.data

        self.assertEqual(
            output_format,
            {
                "amount": 123,
                "normal": 1,
                "account": account_entry.account.id,
                "id": account_entry.id,
                "uuid": str(account_entry.uuid),
                "created": account_entry.created.isoformat(),
            },
        )
