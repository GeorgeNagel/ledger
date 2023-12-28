from django.test import TestCase
from django.http import HttpRequest, HttpResponse

from idempotence.models import IdempotentRequest


class TestIdempotentRequest(TestCase):
    def test_key_from_request_and_client_idempotence_key(self):
        request = HttpRequest()
        request.path = "/some/path"
        request.method = "GET"
        client_idempotence_key = "abcdefg"

        key = IdempotentRequest.objects.key_from_request_and_client_idempotence_key(
            request=request, client_idempotence_key=client_idempotence_key
        )

        self.assertEqual(key, "/some/path:GET:abcdefg")

    def test_create_from_request_and_response(self):
        request = HttpRequest()
        request.path = "/some/path"
        request.method = "POST"
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
        self.assertEqual(idempotent_request.key, "/some/path:POST:abc123")
