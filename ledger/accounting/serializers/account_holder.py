from rest_framework import serializers

from accounting.models.account_holder import AccountHolder
from accounting.serializers.fields import IsoformatDateTimeField


class AccountHolderSerializer(serializers.ModelSerializer):
    created = IsoformatDateTimeField(read_only=True)

    class Meta:
        model = AccountHolder
        fields = ["first_name", "last_name", "created", "id", "uuid"]
