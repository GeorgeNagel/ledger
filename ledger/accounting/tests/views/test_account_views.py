from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from accounting.models.account import Account
from accounting.tests.factories.account_holder import AccountHolderFactory
from accounting.tests.factories.account import AccountFactory
from accounting.serializers.account import AccountSerializer


class TestGetAccount(TestCase):
    def test_get_returns_account(self):
        account = AccountFactory()
        account_url = reverse("get_account", args=[account.id])

        response = self.client.get(account_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), AccountSerializer(account).data)


class TestListAccounts(TestCase):
    def test_get_lists_accounts(self):
        account_holder = AccountHolderFactory()
        account_1 = AccountFactory(account_holder=account_holder, created=timezone.now() - timedelta(days=1))
        account_2 = AccountFactory(account_holder=account_holder)
        list_accounts_url = reverse("list_accounts", args=[account_holder.id])

        response = self.client.get(list_accounts_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), AccountSerializer([account_2, account_1], many=True).data
        )


class TestCreateAccount(TestCase):
    def test_post_creates_new_account(self):
        account_holder = AccountHolderFactory()
        self.assertFalse(Account.objects.exists())
        account_url = reverse("create_account")
        request_data = {"account_type": "checking", "account_holder": account_holder.id, "normal": -1}

        response = self.client.post(
            account_url, data=request_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Account.objects.count(), 1)
        account = Account.objects.first()
        self.assertEqual(response.json(), AccountSerializer(account).data)
        self.assertEqual(account.account_holder, account_holder)
        self.assertEqual(account.account_type, Account.AccountTypes.CHECKING)
        self.assertEqual(account.normal, Account.Normals.CREDIT)
