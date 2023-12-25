from rest_framework import serializers

from accounting.models.account_holder import AccountHolder


class AccountHolderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountHolder
        fields = ["first_name", "last_name"]
