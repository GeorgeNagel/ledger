# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status

# from accounting.models.account import Account
# from accounting.tests.factories.account import AccountFactory
# from accounting.serializers.account import AccountSerializer


# class TestGetAccount(TestCase):
#     def test_get_returns_account(self):
#         account = AccountFactory()
#         account_url = reverse(
#             "get_account", args=[str(account.uuid)]
#         )

#         response = self.client.get(account_url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json(), AccountHolderSerializer(account_holder).data)

# class TestListAccounts(TestCase):
#     def test_get_lists_accounts(self):
#         account_holder = AccountHolderFactory()
#         account_holder_url = reverse(
#             "get_account_holder", args=[str(account_holder.uuid)]
#         )

#         response = self.client.get(account_holder_url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json(), AccountHolderSerializer(account_holder).data)


# class TestCreateAccount(TestCase):
#     def test_post_creates_new_account(self):
#         self.assertFalse(AccountHolder.objects.exists())
#         account_holder_url = reverse("create_account_holder")
#         request_data = {"first_name": "Martin", "last_name": "Phillipps"}

#         response = self.client.post(account_holder_url, data=request_data)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(AccountHolder.objects.count(), 1)
#         account_holder = AccountHolder.objects.first()
#         self.assertEqual(response.json(), AccountHolderSerializer(account_holder).data)
#         self.assertEqual(account_holder.first_name, "Martin")
#         self.assertEqual(account_holder.last_name, "Phillipps")
