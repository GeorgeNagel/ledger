from rest_framework import serializers

from accounting.models.account import Account
from accounting.models.account_holder import AccountHolder
from accounting.serializers.fields import IsoformatDateTimeField, UUIDRelatedField


class AccountSerializer(serializers.ModelSerializer):
    created = IsoformatDateTimeField(read_only=True)
    account_holder = UUIDRelatedField(queryset=AccountHolder.objects.all())

    class Meta:
        model = Account
        fields = ["account_type", "created", "uuid", "normal", "account_holder"]
