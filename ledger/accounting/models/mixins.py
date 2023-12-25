import uuid

from django.db import models


class TimestampedMixin:
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


class IdentifiableMixin:
    """
    Adds an auto-incrementing Id
    """

    id = models.AutoField(primary_key=True, unique=True)
