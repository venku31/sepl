# Copyright (c) 2024, SEPL and contributors
# For license information, please see license.txt

import frappe
from frappe import _

# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data


def get_columns():
	columns = [
		# {
		# 	"label": _("Customer"),
		# 	"fieldname": "customer",
		# 	"fieldtype": "Link",
		# 	"options": "Customer",
		# 	"width": 100,
		# },
		# {"label": _("Id"), "fieldname": "transaction_id", "fieldtype": "Data", "width": 100},
		# {"fieldname": "customer_name", "label": _("Customer Name"), "fieldtype": "data", "width": 80},
		{
			"fieldname": "page_no",
			"label": _("Page No"),
			"fieldtype": "data",
			"width": 80,
		},
		{
			"label": _("Sepl Proposal"),
			"fieldname": "sepl_proposal",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("power_before_conversion_at_port"),
			"fieldname": "power_before_conversion_at_port",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("light_details"),
			"fieldname": "light_details",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("sepl_wattage"),
			"fieldname": "sepl_wattage",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("installed_power_af_conversion"),
			"fieldname": "installed_power_af_conversion",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("location"),
			"fieldname": "location",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("Qty"),
			"fieldname": "qty",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("power_after_conversion_at_sea"),
			"fieldname": "power_after_conversion_at_sea",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("wattage"),
			"fieldname": "wattage",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("usage_factor"),
			"fieldname": "usage_factor",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("power_after_conversion_at_port"),
			"fieldname": "power_after_conversion_at_port",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("fixtures"),
			"fieldname": "fixtures",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("installed_bf_power_conversion"),
			"fieldname": "installed_bf_power_conversion",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("power_consumption_per_year_before_conversion_in_kwh"),
			"fieldname": "power_consumption_per_year_before_conversion_in_kwh",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("units"),
			"fieldname": "units",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("power_before_conversion_at_sea"),
			"fieldname": "power_before_conversion_at_sea",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("power_consumption_per_year_after_conversion_in_kwh"),
			"fieldname": "power_consumption_per_year_after_conversion_in_kwh",
			"fieldtype": "Data",
			"width": 120,
		},
	]
	return columns


def get_data(filters):
	return frappe.db.sql(
		"""
		select
		led.customer,
		led.customer_name,
		led.date ,
		led.name as transaction_id,
		ledt.page_no,
		ledt.sepl_proposal,
		ledt.power_before_conversion_at_port,
		ledt.light_details,
		ledt.sepl_wattage,
		ledt.installed_power_af_conversion,
		ledt.location,
		ledt.qty,
		ledt.power_after_conversion_at_sea,
		ledt.wattage,
		ledt.usage_factor,
		ledt.power_after_conversion_at_port,
		ledt.fixtures,
		ledt.installed_bf_power_conversion,
		ledt.power_consumption_per_year_before_conversion_in_kwh,
		ledt.units,
		ledt.power_before_conversion_at_sea,
		ledt.power_consumption_per_year_after_conversion_in_kwh
        from `tabLED Conversion Proposal` led join `tabLED Conversion Proposal Details` ledt ON(led.name=ledt.parent)
		WHERE led.customer=%(customer)s
			{conditions}
		ORDER BY
			led.date,led.customer asc """.format(
			conditions=get_conditions(filters)
		),
		filters,
		as_dict=1,
	)


def get_conditions(filters):
	conditions = []

	
	if filters.get("transaction_id"):
		conditions.append(" and led.name=%(transaction_id)s")

	return " ".join(conditions) if conditions else ""