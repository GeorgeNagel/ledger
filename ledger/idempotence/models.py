from django.db import models
from django.db.models.functions import Now


class IdempotentRequestManager(models.Manager):
    def create_from_request_and_response(
        self, request=None, response=None, client_idempotence_key=None
    ):
        idempotent_request = IdempotentRequest(
            key="{}:{}:{}".format(request.path, request.method, client_idempotence_key),
            response_body=response.content,
            response_status=response.status_code,
            response_headers=dict(response.headers),
        )
        idempotent_request.save()
        return idempotent_request


class IdempotentRequest(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=Now())
    key = models.CharField(max_length=256, unique=True)
    response_body = models.TextField()
    response_headers = models.JSONField()
    response_status = models.IntegerField()

    objects = IdempotentRequestManager()
