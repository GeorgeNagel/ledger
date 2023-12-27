import uuid

from django.db import models


class TimestampedMixin(models.Model):
    """
    Adds creation and modification timestamps
    """

    # Tracks when this record was inserted in the database
    # Note: This should be used for tracking/debugging purposes
    # and should not be used to drive business logic
    # If you need to drive business logic off of a date,
    # add a field for that purpose, e.g. 'effective_date'.
    # This allows new records to be created for previous dates
    # within the current accounting period while maintaining
    # an accurate paper trail of when the entries were created
    created = models.DateTimeField(auto_now_add=True)

    # Tracks when this record was updated
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class IdentifiableMixin(models.Model):
    """
    Adds an auto-incrementing Id and UUID
    """

    # Auto-incrementing IDs should not be exposed to end-users
    # e.g. in URLs or API responses, as a potential attacker
    # could guess at possible other values of IDs due
    # to their auto-incrementing nature.
    id = models.AutoField(primary_key=True, unique=True)

    # The UUID allows unique identification of the model
    # e.g. in URLs or API responses, while not providing
    # potential attackers any information about possible
    # values for other UUIDs.
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)

    class Meta:
        abstract=True