from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from accounting.models.account_holder import AccountHolder
from accounting.tests.factories.account_holder import AccountHolderFactory
from accounting.serializers.account_holder import AccountHolderSerializer


class TestGetAccountHolder(TestCase):
    def test_get_returns_account_holder(self):
        account_holder = AccountHolderFactory()
        account_holder_url = reverse("get_account_holder", args=[account_holder.id])

        response = self.client.get(account_holder_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), AccountHolderSerializer(account_holder).data)


class TestCreateAccountHolder(TestCase):
    def test_post_creates_new_account_holder(self):
        self.assertFalse(AccountHolder.objects.exists())
        account_holder_url = reverse("create_account_holder")
        request_data = {"first_name": "Martin", "last_name": "Phillipps"}

        response = self.client.post(account_holder_url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AccountHolder.objects.count(), 1)
        account_holder = AccountHolder.objects.first()
        self.assertEqual(response.json(), AccountHolderSerializer(account_holder).data)
        self.assertEqual(account_holder.first_name, "Martin")
        self.assertEqual(account_holder.last_name, "Phillipps")
