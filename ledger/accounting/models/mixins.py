import uuid

from django.db import models


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
        abstract = True
