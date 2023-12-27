from django.urls import path

from accounting.views.account_holder import get_account_holder, create_account_holder
from accounting.views.journal_entry import get_journal_entry, create_journal_entry


urlpatterns = [
    path("account_holder/<uuid:uuid>", get_account_holder, name="get_account_holder"),
    path("account_holder/", create_account_holder, name="create_account_holder"),
    path("journal_entry/<uuid:uuid>", get_journal_entry, name="get_journal_entry"),
    path("journal_entry/", create_journal_entry, name="create_journal_entry"),
]
