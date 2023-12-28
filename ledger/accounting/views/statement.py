import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from accounting.models.statement import Statement
from accounting.serializers.statement import StatementSerializer


@require_http_methods(["GET"])
def get_statement(request, id, *args, **kwargs):
    statement = get_object_or_404(Statement, id=id)
    serializer = StatementSerializer(statement)
    return JsonResponse(serializer.data)


@require_http_methods(["GET"])
def list_statements(request, account_id, *args, **kwargs):
    statements = Statement.objects.filter(account_id=account_id).order_by("-created")
    serializer = StatementSerializer(statements, many=True)
    return JsonResponse(serializer.data, safe=False)


@require_http_methods(["POST"])
def create_statement(request, *args, **kwargs):
    data = json.loads(request.body)
    serializer = StatementSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse(serializer.data, status=201)
