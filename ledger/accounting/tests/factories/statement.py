from django.utils import timezone
import factory

from accounting.tests.factories.account import AccountFactory


class StatementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounting.Statement"

    balance = 0
    account = factory.SubFactory(AccountFactory)
    date_close = factory.lazy_attribute(lambda obj: timezone.now())
