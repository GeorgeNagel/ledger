from django.test import TestCase

from accounting.tests.factories.account_holder import AccountHolderFactory
from accounting.serializers.account_holder import AccountHolderSerializer
from accounting.models.account_holder import AccountHolder


class TestAccountHolderSerializer(TestCase):
    def test_output_format(self):
        self.maxDiff = None
        account_holder = AccountHolderFactory(first_name="Ian", last_name="Curtis")
        serializer = AccountHolderSerializer(account_holder)

        output_format = serializer.data

        self.assertEqual(
            output_format,
            {
                "first_name": "Ian",
                "last_name": "Curtis",
                "uuid": str(account_holder.uuid),
                "created": account_holder.created.isoformat(),
            },
        )

    def test_save_creates_account_holder(self):
        self.assertEqual(AccountHolder.objects.count(), 0)
        data = {"first_name": "Bernard", "last_name": "Sumner"}
        serializer = AccountHolderSerializer(data=data)

        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        serializer.save()

        self.assertEqual(AccountHolder.objects.count(), 1)
        account_holder = AccountHolder.objects.first()
        self.assertEqual(account_holder.first_name, "Bernard")
        self.assertEqual(account_holder.last_name, "Sumner")
