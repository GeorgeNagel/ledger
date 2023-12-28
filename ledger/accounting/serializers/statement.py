from rest_framework import serializers

from accounting.models.statement import Statement
from accounting.serializers.fields import IsoformatDateTimeField


class StatementSerializer(serializers.ModelSerializer):
    created = IsoformatDateTimeField(read_only=True)
    date_close = IsoformatDateTimeField()

    class Meta:
        model = Statement
        fields = ["balance", "created", "date_close", "uuid", "id", "account"]
