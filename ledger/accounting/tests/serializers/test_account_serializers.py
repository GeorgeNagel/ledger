from django.test import TestCase

from accounting.tests.factories.account import AccountFactory
from accounting.tests.factories.account_holder import AccountHolderFactory
from accounting.serializers.account import AccountSerializer
from accounting.models.account import Account


class TestAccountSerializer(TestCase):
    def test_output_format(self):
        account = AccountFactory(
            account_type=Account.AccountTypes.CHECKING, normal=Account.Normals.DEBIT
        )
        serializer = AccountSerializer(account)

        output_format = serializer.data

        self.assertEqual(
            output_format,
            {
                "account_type": "checking",
                "normal": 1,
                "id": account.id,
                "uuid": str(account.uuid),
                "created": account.created.isoformat(),
                "account_holder": account.account_holder.id,
            },
        )

    def test_save_creates_account(self):
        self.assertEqual(Account.objects.count(), 0)
        account_holder = AccountHolderFactory()
        data = {
            "account_type": "checking",
            "normal": -1,
            "account_holder": account_holder.id,
        }
        serializer = AccountSerializer(data=data)

        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        serializer.save()

        self.assertEqual(Account.objects.count(), 1)
        account = Account.objects.first()
        self.assertEqual(account.account_holder, account_holder)
        self.assertEqual(account.normal, Account.Normals.CREDIT)
        self.assertEqual(account.account_type, Account.AccountTypes.CHECKING)
