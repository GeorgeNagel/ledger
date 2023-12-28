from django.urls import path

from accounting.views.account import get_account, list_accounts, create_account
from accounting.views.account_holder import get_account_holder, create_account_holder
from accounting.views.journal_entry import get_journal_entry, create_journal_entry
from accounting.views.statement import get_statement, create_statement, list_statements


urlpatterns = [
    path("account/<int:id>", get_account, name="get_account"),
    path("account/<int:account_id>/statements", list_statements, name="list_statements"),
    path("account/", create_account, name="create_account"),
    path("account_holder/<int:account_holder_id>/accounts", list_accounts, name="list_accounts"),
    path("account_holder/<int:id>", get_account_holder, name="get_account_holder"),
    path("account_holder/", create_account_holder, name="create_account_holder"),
    path("journal_entry/<int:id>", get_journal_entry, name="get_journal_entry"),
    path("journal_entry/", create_journal_entry, name="create_journal_entry"),
    path("statement/<int:id>", get_statement, name="get_statement"),
    path("statement/", create_statement, name="create_statement"),
]
