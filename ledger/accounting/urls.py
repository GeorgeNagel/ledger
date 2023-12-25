from django.urls import path

from accounting.views.account_holder import get_account_holder, create_account_holder


urlpatterns = [
    path("account_holder/<int:id>", get_account_holder, name="get_account_holder"),
    path("account_holder/", create_account_holder, name="create_account_holder"),
]
