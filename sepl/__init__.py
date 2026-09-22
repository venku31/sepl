__version__ = "0.0.1"


from erpnext.accounts.report import accounts_receivable
from erpnext.stock.report.stock_balance import stock_balance
from sepl.reports.accounts_receivable_override import custom_execute
from sepl.reports.stock_balance_override import execute as stock_balance_execute


accounts_receivable.accounts_receivable.execute = custom_execute
stock_balance.execute = stock_balance_execute
