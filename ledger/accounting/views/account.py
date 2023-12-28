import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from accounting.models.account import Account
from accounting.serializers.account import AccountSerializer


@require_http_methods(["GET"])
def get_account(request, id, *args, **kwargs):
    account = get_object_or_404(Account, id=id)
    serializer = AccountSerializer(account)
    return JsonResponse(serializer.data)


@require_http_methods(["GET"])
def list_accounts(request, account_holder_id, *args, **kwargs):
    accounts = Account.objects.filter(account_holder_id=account_holder_id).order_by(
        "-created"
    )
    serializer = AccountSerializer(accounts, many=True)
    return JsonResponse(serializer.data, safe=False)


@require_http_methods(["POST"])
def create_account(request, *args, **kwargs):
    data = json.loads(request.body)
    serializer = AccountSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse(serializer.data, status=201)
