# Copyright (c) 2024, SEPL and contributors
# For license information, please see license.txt

import frappe
from frappe import _

# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
def execute(filters=None):
	validate_filters(filters)
	columns, data = get_columns(), get_data(filters)
	chart = get_chart_data(data)
	# return columns, data,None, chart
	# columns = get_columns()
	# data = get_data(filters)
	
	report_summary = get_report_summary(data)
	return columns, data, None, chart, report_summary
	# return columns, data


def validate_filters(filters):
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date cannot be greater than To Date"))

def get_columns():
	columns = [
		{
			"fieldname": "quotation",
			"label": _("Quotation"),
			"fieldtype": "Link",
			"options": "Quotation",
			"width": 250,
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 80,
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer_name",
			"fieldtype": "Data",
			"width": 250,
		},
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 150,
		},
				
							
	]
	return columns


def get_data(filters):
	return frappe.db.sql(
		"""
		Select name as quotation,
		party_name as customer ,
		customer_name,
		transaction_date as date,
		status,
		owner as created_by
		from `tabQuotation` 
		WHERE DATE(transaction_date) BETWEEN %(from_date)s AND %(to_date)s
			{conditions}
		ORDER BY
			transaction_date desc """.format(
			conditions=get_conditions(filters)
		),
		filters,
		as_dict=1,
	)


def get_conditions(filters):
	conditions = []

	if filters.get("customer"):
		conditions.append(" and party_name=%(customer)s")

	if filters.get("status"):
		conditions.append(" and status =%(status)s")

	
	return " ".join(conditions) if conditions else ""

def get_chart_data(data):
	if not data:
		return None

	draft = 0
	open  = 0
	registered =0
	partially_ordered =0
	ordered = 0

	for entry in data:
		if entry.status == "Draft":
			draft += 1
		elif entry.status == "Open":
			open += 1
		elif entry.status == "Partially Ordered":
			partially_ordered += 1
		elif entry.status == "Ordered":
			ordered += 1
		
		else:
			registered += 1

	chart = {
		"data": {
			# "labels": [_("pending"), _("registered"),_("pending_procurement_review"),_("pending_prequalification"),_("approved"),_("rejected")],
			"datasets": [{"name": _("Status"), "values": [draft,open,partially_ordered,ordered]}],
		},
		"type": "donut",
		"colors": ["red", "red", "yellow","green"],
	}

	return chart


def get_report_summary(data):
	if not data:
		return None

	total = len(data)
	draft = len([entry.name for entry in data if entry.status == "Draft"])
	open = len([entry.name for entry in data if entry.status in ["Open" ]])
	partially_ordered = len([entry.name for entry in data if entry.status == "Partially Ordered"])
	ordered = len([entry.name for entry in data if entry.status in ["Ordered"]])

	return [
		{
			"value": total,
			"label": _("Total"),
			"indicator": "Blue" ,
			"datatype": "Int",
		},
		{
			"value": draft,
			"label": _("Draft"),
			"indicator": "Red",
			"datatype": "Int",
		},
		{
			"value": open,
			"label": _("Open"),
			"indicator": "Red",
			"datatype": "Int",
		},
		{
			"value": partially_ordered,
			"label": _("Partially Ordered"),
			"indicator": "Green",
			"datatype": "Int",
		},
		{
			"value": ordered,
			"label": _("Ordered"),
			"indicator": "Green",
			"datatype": "Int",
		},
	]		