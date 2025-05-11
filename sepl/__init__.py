__version__ = "0.0.1"


from erpnext.accounts.report import accounts_receivable
from sepl.reports.accounts_receivable_override import custom_execute


accounts_receivable.accounts_receivable.execute = custom_execute
