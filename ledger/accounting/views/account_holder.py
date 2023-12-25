from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from accounting.models.account_holder import AccountHolder
from accounting.serializers.account_holder import AccountHolderSerializer


@require_http_methods(["GET"])
def get_account_holder(request, id, *args, **kwargs):
    account_holder = get_object_or_404(AccountHolder, id=id)
    serializer = AccountHolderSerializer(account_holder)
    return JsonResponse(serializer.data)


@require_http_methods(["POST"])
def create_account_holder(request, *args, **kwargs):
    serializer = AccountHolderSerializer(data=request.POST)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse(serializer.data)
