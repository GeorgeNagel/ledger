from unittest.mock import Mock, call

from django.test import TestCase
from django.http import HttpRequest, HttpResponse

from idempotence.models import IdempotentRequest
from idempotence.middleware import IdempotenceMiddleware


class IdempotenceMiddlewareTestCase(TestCase):
    def test_doesnt_create_model_if_idempotence_header_unset(self):
        mock_get_response = Mock()
        middleware = IdempotenceMiddleware(get_response=mock_get_response)
        middleware.__call__(HttpRequest())
        self.assertFalse(IdempotentRequest.objects.exists())

    def test_creates_model_when_idempotence_header_set(self):
        mock_get_response = Mock()
        mock_get_response.return_value = HttpResponse()
        middleware = IdempotenceMiddleware(get_response=mock_get_response)
        request = HttpRequest()
        request.headers = {"Idempotence-Key": "abc"}
        middleware.__call__(request)
        self.assertTrue(IdempotentRequest.objects.exists())

    def test_repeat_requests_with_same_key_only_create_one_model(self):
        mock_get_response = Mock()
        mock_get_response.return_value = HttpResponse()
        middleware = IdempotenceMiddleware(get_response=mock_get_response)
        request = HttpRequest()
        request.headers = {"Idempotence-Key": "abc"}
        middleware.__call__(request)
        middleware.__call__(request)
        self.assertEqual(IdempotentRequest.objects.count(), 1)

    def test_repeat_requests_with_same_key_only_make_request_once(self):
        mock_get_response = Mock()
        mock_get_response.return_value = HttpResponse()
        middleware = IdempotenceMiddleware(get_response=mock_get_response)
        request = HttpRequest()
        request.headers = {"Idempotence-Key": "abc"}
        middleware.__call__(request)
        middleware.__call__(request)
        self.assertEqual(len(mock_get_response.mock_calls), 1)

    def test_repeat_requests_with_same_key_return_original_response_data(self):
        mock_get_response = Mock()
        mock_get_response.return_value = HttpResponse()
        middleware = IdempotenceMiddleware(get_response=mock_get_response)
        request = HttpRequest()
        request.headers = {"Idempotence-Key": "abc"}
        response_1 = middleware.__call__(request)
        response_2 = middleware.__call__(request)
        self.assertEqual(response_1.status_code, response_2.status_code)
        self.assertEqual(response_1.headers, response_2.headers)
        self.assertEqual(response_1.content, response_2.content)

    def test_repeat_requests_with_different_key_create_new_model(self):
        mock_get_response = Mock()
        mock_get_response.return_value = HttpResponse()
        middleware = IdempotenceMiddleware(get_response=mock_get_response)
        request_1 = HttpRequest()
        request_1.headers = {"Idempotence-Key": "abc"}
        request_2 = HttpRequest()
        request_2.headers = {"Idempotence-Key": "def"}
        middleware.__call__(request_1)
        middleware.__call__(request_2)
        self.assertEqual(IdempotentRequest.objects.count(), 2)

    def test_repeat_requests_with_different_key_make_request_again(self):
        mock_get_response = Mock()
        mock_get_response.return_value = HttpResponse()
        middleware = IdempotenceMiddleware(get_response=mock_get_response)
        request_1 = HttpRequest()
        request_1.headers = {"Idempotence-Key": "abc"}
        request_2 = HttpRequest()
        request_2.headers = {"Idempotence-Key": "def"}
        middleware.__call__(request_1)
        middleware.__call__(request_2)
        self.assertEqual(len(mock_get_response.mock_calls), 2)
