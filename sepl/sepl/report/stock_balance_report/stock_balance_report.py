import frappe
from frappe import _
from frappe.utils import flt, nowdate

from erpnext.stock.report.stock_ageing.stock_ageing import FIFOSlots, get_average_age
from erpnext.stock.report.stock_analytics.stock_analytics import get_stock_ledger_entries
from erpnext.stock.report.warehouse_wise_item_balance_age_and_value.warehouse_wise_item_balance_age_and_value import (
	get_item_warehouse_map,
)


def execute(filters=None):
	filters = frappe._dict(filters or {})
	filters.from_date = "1900-01-01"
	filters.to_date = nowdate()
	company = filters.get("company") or frappe.defaults.get_user_default("Company")
	filters.company = company
	warehouses = get_warehouses(company, filters)
	items = frappe.get_all(
		"Item",
		filters=get_item_filters(filters),
		fields=["name", "item_name", "item_group"],
		order_by="name",
	)

	item_codes = [item.name for item in items]
	stock_ledger_entries = get_stock_ledger_entries(filters, item_codes)
	item_warehouse_map = get_item_warehouse_map(filters, stock_ledger_entries)
	balances = {
		(item_code, warehouse): qty_dict.bal_qty
		for (_company, item_code, warehouse), qty_dict in item_warehouse_map.items()
	}
	warehouses = [
		warehouse
		for warehouse in warehouses
		if flt(sum(balances.get((item.name, warehouse.name), 0) or 0 for item in items)) != 0
	]

	columns = [
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 260},
		{"label": _("Item Group"), "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 150},
		{"label": _("Age"), "fieldname": "age", "fieldtype": "Float", "width": 100},
		{"label": _("Total Qty"), "fieldname": "total_qty", "fieldtype": "Float", "width": 120},
	]
	for warehouse in warehouses:
		columns.append({
			"label": _("{0} UNITS").format(warehouse.name),
			"fieldname": "warehouse_" + frappe.scrub(warehouse.name),
			"fieldtype": "Float",
			"width": 160,
		})

	item_ageing = FIFOSlots(filters).generate()
	data = []
	for item in items:
		row = {"item_code": item.name, "item_name": item.item_name, "item_group": item.item_group}
		for warehouse in warehouses:
			fieldname = "warehouse_" + frappe.scrub(warehouse.name)
			row[fieldname] = balances.get((item.name, warehouse.name), 0)
		row["total_qty"] = sum(row.get("warehouse_" + frappe.scrub(warehouse.name), 0) or 0 for warehouse in warehouses)
		fifo_queue = item_ageing.get(item.name, {}).get("fifo_queue", [])
		row["age"] = get_average_age(fifo_queue, filters.to_date) if fifo_queue else 0
		data.append(row)

	return columns, data


def get_item_filters(filters):
	item_filters = {"disabled": 0, "is_stock_item": 1}
	if filters.get("item_code"):
		item_filters["name"] = filters.item_code
	if filters.get("item_group"):
		item_filters["item_group"] = filters.item_group
	return item_filters


def get_warehouses(company, filters):
	warehouse_filters = {"is_group": 0, "disabled": 0}
	if company:
		warehouse_filters["company"] = company
	if filters.get("warehouse"):
		warehouse_filters["name"] = filters.warehouse
	warehouses = frappe.get_all(
		"Warehouse",
		filters=warehouse_filters,
		fields=["name"],
		order_by="name",
	)
	from frappe.core.doctype.user_permission.user_permission import get_permitted_documents

	permitted = get_permitted_documents("Warehouse")
	if permitted:
		allowed = set(permitted)
		warehouses = [warehouse for warehouse in warehouses if warehouse.name in allowed]
	return warehouses
