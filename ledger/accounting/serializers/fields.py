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


class UUIDRelatedField(serializers.RelatedField):
    def to_representation(self, model):
        return str(model.uuid)

    def to_internal_value(self, data):
        return self.queryset.get(uuid=data)
