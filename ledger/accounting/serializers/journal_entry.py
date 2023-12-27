from rest_framework import serializers

from accounting.models.journal_entry import JournalEntry
from accounting.models.account_entry import AccountEntry
from accounting.serializers.fields import IsoformatDateTimeField
from accounting.serializers.account_entry import AccountEntrySerializer


class JournalEntrySerializer(serializers.ModelSerializer):
    created = IsoformatDateTimeField(read_only=True)
    account_entries = AccountEntrySerializer(many=True)

    class Meta:
        model = JournalEntry
        fields = ["created", "account_entries", "id", "uuid"]

    def create(self, validated_data):
        account_entry_dicts = validated_data.pop("account_entries")
        JournalEntry.objects.create_from_account_entry_dicts(
            account_entry_dicts=account_entry_dicts
        )


class CreateJournalEntrySerializer(serializers.ModelSerializer):
    class CreateAccountEntrySerializer(serializers.ModelSerializer):
        account = serializers.IntegerField()

        class Meta:
            model = AccountEntry
            fields = ["amount", "normal", "account"]

    account_entries = CreateAccountEntrySerializer(many=True)

    class Meta:
        model = JournalEntry
        fields = ["account_entries"]

    def create(self, validated_data):
        account_entry_dicts = validated_data.pop("account_entries")
        journal_entry = JournalEntry.objects.create_from_account_entry_dicts(
            account_entry_dicts=account_entry_dicts
        )
        return journal_entry
