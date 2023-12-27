from datetime import datetime, timezone
from unittest import TestCase

from accounting.models.account_holder import AccountHolder
from accounting.serializers.fields import IsoformatDateTimeField, UUIDRelatedField
from accounting.tests.factories.account_holder import AccountHolderFactory


class TestIsoformatDateTime(TestCase):
    def test_to_representation(self):
        value = datetime(2000, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        field = IsoformatDateTimeField()

        representation = field.to_representation(value)

        self.assertEqual(representation, "2000-01-02T03:04:05+00:00")

    def test_to_internal_value(self):
        representation = "2000-01-02T03:04:05+00:00"
        field = IsoformatDateTimeField()

        value = field.to_internal_value(representation)

        self.assertEqual(value, datetime(2000, 1, 2, 3, 4, 5, tzinfo=timezone.utc))


class TestUUIDRelatedField(TestCase):
    def test_to_representation(self):
        account_holder = AccountHolderFactory()
        field = UUIDRelatedField(queryset=AccountHolder.objects.all())

        representation = field.to_representation(account_holder)

        self.assertEqual(representation, str(account_holder.uuid))

    def test_to_internal_value(self):
        account_holder = AccountHolderFactory()
        field = UUIDRelatedField(queryset=AccountHolder.objects.all())

        value = field.to_internal_value(str(account_holder.uuid))

        self.assertEqual(value, account_holder)
