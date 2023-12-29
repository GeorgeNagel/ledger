from django.db import models
from django.db.models.functions import Now


class IdempotentRequestManager(models.Manager):
    def key_from_request_and_client_idempotence_key(
        self, request=None, client_idempotence_key=None
    ):
        key = "{}:{}:{}".format(request.path, request.method, client_idempotence_key)
        return key

    def create_from_request_and_response(
        self, request=None, response=None, client_idempotence_key=None
    ):
        key = IdempotentRequest.objects.key_from_request_and_client_idempotence_key(
            request=request, client_idempotence_key=client_idempotence_key
        )
        idempotent_request = IdempotentRequest(
            key=key,
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
    response_body = models.BinaryField()
    response_headers = models.JSONField()
    response_status = models.IntegerField()

    objects = IdempotentRequestManager()
