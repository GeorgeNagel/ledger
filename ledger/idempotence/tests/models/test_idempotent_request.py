from django.test import TestCase
from django.http import HttpRequest, HttpResponse

from idempotence.models import IdempotentRequest


class TestIdempotentRequest(TestCase):
    def test_create_from_request_and_response(self):
        request = HttpRequest()
        request.path = '/some/path'
        request.method = 'POST'
        response = HttpResponse(
            content=b"Hello there!",
            status=404,
            headers={"Content-Type": "application/json", "x-foo": "bar-baz"},
        )

        idempotent_request = IdempotentRequest.objects.create_from_request_and_response(
            request=request, response=response, client_idempotence_key="abc123"
        )
        self.assertEqual(idempotent_request.response_status, 404)
        self.assertEqual(idempotent_request.response_body, b"Hello there!")
        self.assertEqual(
            idempotent_request.response_headers,
            {"Content-Type": "application/json", "x-foo": "bar-baz"},
        )
        self.assertEqual(idempotent_request.key, '/some/path:POST:abc123')
