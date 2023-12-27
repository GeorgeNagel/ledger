from datetime import datetime

from rest_framework import serializers


class IsoformatDateTimeField(serializers.Field):
    """
    ISO 8601 formatted datetimes
    """

    def to_representation(self, value):
        return value.isoformat()

    def to_internal_value(self, data):
        dt = datetime.fromisoformat(data)
        return dt
