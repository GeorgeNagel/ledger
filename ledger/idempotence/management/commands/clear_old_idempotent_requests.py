from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from idempotence.models import IdempotentRequest


class Command(BaseCommand):
    """
    We don't need to keep IdempotentRequests around forever.
    Instead, we can just guarantee idempotency for 30 minutes after
    the initial request.
    """

    help = "Delete IdempotentResponses older than 30 minutes"

    def handle(self, *args, **options):
        thirty_minutes_ago = timezone.now() - timedelta(minutes=30)
        old_idempotent_requests = IdempotentRequest.objects.filter(
            created__lt=thirty_minutes_ago
        )
        count = old_idempotent_requests.count()
        old_idempotent_requests.delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully removed {} old IdempotentResponses ".format(count)
            )
        )
