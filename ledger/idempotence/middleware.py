from django.http import HttpResponse

from idempotence.models import IdempotentRequest


class IdempotenceMiddleware:
    def __init__(self, get_response):
        # Initialize the middleware factory
        # See: https://docs.djangoproject.com/en/5.0/topics/http/middleware/
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        client_idempotence_key = request.headers.get("Idempotence-Key")
        existing_idempotent_request = None
        if client_idempotence_key:
            idempotence_key = (
                IdempotentRequest.objects.key_from_request_and_client_idempotence_key(
                    request=request, client_idempotence_key=client_idempotence_key
                )
            )
            try:
                existing_idempotent_request = IdempotentRequest.objects.get(
                    key=idempotence_key
                )
                response = HttpResponse()
                response.content = existing_idempotent_request.response_body
                response.status = existing_idempotent_request.response_status
                response.headers = existing_idempotent_request.response_headers
                return response
            except IdempotentRequest.DoesNotExist:
                pass

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if client_idempotence_key and not existing_idempotent_request:
            IdempotentRequest.objects.create_from_request_and_response(
                request=request,
                response=response,
                client_idempotence_key=client_idempotence_key,
            )

        return response
