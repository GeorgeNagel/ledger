import factory


class AccountHolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounting.AccountHolder"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
