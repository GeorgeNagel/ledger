from idempotence.models import IdempotentRequest


class IdempotenceMiddleware:
    def __init__(self, get_response):
        # Initialize the middleware factory
        # See: https://docs.djangoproject.com/en/5.0/topics/http/middleware/
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        client_idempotence_key = request.headers.get("Idempotence-Key")
        if client_idempotence_key:
            IdempotentRequest.objects.create_from_request_and_response(
                request=request,
                response=response,
                client_idempotence_key=client_idempotence_key,
            )

        return response
