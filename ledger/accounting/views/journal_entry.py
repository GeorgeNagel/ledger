import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from accounting.models.journal_entry import JournalEntry
from accounting.serializers.journal_entry import (
    JournalEntrySerializer,
    CreateJournalEntrySerializer,
)


@require_http_methods(["GET"])
def get_journal_entry(request, id, *args, **kwargs):
    journal_entry = get_object_or_404(JournalEntry, id=id)
    serializer = JournalEntrySerializer(journal_entry)
    return JsonResponse(serializer.data)


@require_http_methods(["POST"])
def create_journal_entry(request, *args, **kwargs):
    data = json.loads(request.body)
    create_journal_entry_serializer = CreateJournalEntrySerializer(data=data)
    create_journal_entry_serializer.is_valid(raise_exception=True)
    journal_entry = create_journal_entry_serializer.save()
    journal_entry_serializer = JournalEntrySerializer(journal_entry)
    return JsonResponse(journal_entry_serializer.data, status=201)
