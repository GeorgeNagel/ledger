from django.utils import timezone
import factory


class JournalEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounting.JournalEntry"
