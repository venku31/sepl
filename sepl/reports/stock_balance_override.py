"""SEPL customisation for the ERPNext Stock Balance report."""

import frappe

from erpnext.stock.report.stock_balance.stock_balance import StockBalanceReport as BaseStockBalanceReport


def execute(filters=None):
	"""Run Stock Balance while excluding disabled Item records."""
	return StockBalanceReport(frappe._dict(filters or {})).run()


class StockBalanceReport(BaseStockBalanceReport):
	def apply_items_filters(self, query, item_table):
		"""Restrict ledger entries to enabled items."""
		query = super().apply_items_filters(query, item_table)
		return query.where(item_table.disabled == 0)

	def prepare_opening_data_from_closing_balance(self):
		"""Exclude disabled items stored in a Closing Stock Balance."""
		super().prepare_opening_data_from_closing_balance()
		if not self.opening_data:
			return

		enabled_items = {
			item.name
			for item in frappe.get_all(
				"Item",
				filters={
					"disabled": 0,
					"name": ("in", list({key[1] for key in self.opening_data})),
				},
				fields=["name"],
			)
		}
		self.opening_data = frappe._dict(
			{key: entry for key, entry in self.opening_data.items() if key[1] in enabled_items}
		)
