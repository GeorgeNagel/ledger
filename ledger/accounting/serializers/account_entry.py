from rest_framework import serializers

from accounting.models.account_entry import AccountEntry
from accounting.serializers.fields import IsoformatDateTimeField


class AccountEntrySerializer(serializers.ModelSerializer):
    created = IsoformatDateTimeField(read_only=True)

    class Meta:
        model = AccountEntry
        fields = ["amount", "normal", "created", "id", "uuid", "account"]
