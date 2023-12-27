from rest_framework import serializers

from accounting.models.account import Account
from accounting.serializers.fields import IsoformatDateTimeField


class AccountSerializer(serializers.ModelSerializer):
    created = IsoformatDateTimeField(read_only=True)

    class Meta:
        model = Account
        fields = ["account_type", "created", "id", "uuid", "normal", "account_holder"]
