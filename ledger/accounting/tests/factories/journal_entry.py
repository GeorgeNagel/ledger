from django.utils import timezone
import factory

from accounting.models.account_entry import AccountEntry


class JournalEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounting.JournalEntry"


class JournalEntryWithDebitAndCredit(factory.django.DjangoModelFactory):
    amount = 1
    created = factory.lazy_attribute(lambda obj: timezone.now())
    debit = factory.RelatedFactory(
        "accounting.tests.factories.account_entry.AccountEntryFactory",
        factory_related_name="journal_entry",
        normal=AccountEntry.Normals.DEBIT,
        amount=factory.SelfAttribute("..amount"),
        created=factory.SelfAttribute("..created"),
    )
    credit = factory.RelatedFactory(
        "accounting.tests.factories.account_entry.AccountEntryFactory",
        factory_related_name="journal_entry",
        normal=AccountEntry.Normals.CREDIT,
        amount=factory.SelfAttribute("..amount"),
        created=factory.SelfAttribute("..created"),
    )

    class Meta:
        model = "accounting.JournalEntry"
        exclude = ("debit", "credit", "amount", "created")
