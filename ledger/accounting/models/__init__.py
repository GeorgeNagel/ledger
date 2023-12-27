# Models have to be accessible via `from appname.models import *` for discovery for migrations
from accounting.models.account import Account as _Account
from accounting.models.account_holder import AccountHolder as _AccountHolder
from accounting.models.journal_entry import JournalEntry as _JournalEntry
from accounting.models.account_entry import (
    AccountEntry as _AccountEntry,
)
from accounting.models.statement import Statement as _Statement
