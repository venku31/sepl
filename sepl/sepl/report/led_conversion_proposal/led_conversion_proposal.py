# Copyright (c) 2024, SEPL and contributors
# For license information, please see license.txt
import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {"fieldname": "customer", "label": _("Customer"), "fieldtype": "Data", "width": 80},
        {"fieldname": "date", "label": _("Date"), "fieldtype": "Date", "width": 80},
        {"fieldname": "page_no", "label": _("Page No"), "fieldtype": "Data", "width": 80},
        {"fieldname": "sepl_proposal", "label": _("SEPL Proposal"), "fieldtype": "Data", "width": 120},
        {"fieldname": "power_before_conversion_at_port", "label": _("Power Before Conversion (Port)"), "fieldtype": "Float", "width": 120},
        {"fieldname": "light_details", "label": _("Light Details"), "fieldtype": "Data", "width": 120},
        {"fieldname": "sepl_wattage", "label": _("SEPL Wattage"), "fieldtype": "Float", "width": 120},
        {"fieldname": "installed_power_af_conversion", "label": _("Installed Power After Conversion"), "fieldtype": "Float", "width": 120},
        {"fieldname": "location", "label": _("Location"), "fieldtype": "Data", "width": 120},
        {"fieldname": "qty", "label": _("Qty"), "fieldtype": "Int", "width": 120},
        {"fieldname": "power_after_conversion_at_sea", "label": _("Power After Conversion (Sea)"), "fieldtype": "Float", "width": 120},
        {"fieldname": "wattage", "label": _("Wattage"), "fieldtype": "Float", "width": 120},
        {"fieldname": "usage_factor", "label": _("Usage Factor"), "fieldtype": "Float", "width": 120},
        {"fieldname": "power_after_conversion_at_port", "label": _("Power After Conversion (Port)"), "fieldtype": "Float", "width": 120},
        {"fieldname": "fixtures", "label": _("Fixtures"), "fieldtype": "Data", "width": 120},
        {"fieldname": "installed_bf_power_conversion", "label": _("Installed Before Conversion Power"), "fieldtype": "Float", "width": 120},
        {"fieldname": "power_consumption_per_year_before_conversion_in_kwh", "label": _("Annual Power Consumption Before (kWh)"), "fieldtype": "Float", "width": 120},
        {"fieldname": "units", "label": _("Units"), "fieldtype": "Int", "width": 120},
        {"fieldname": "power_before_conversion_at_sea", "label": _("Power Before Conversion (Sea)"), "fieldtype": "Float", "width": 120},
        {"fieldname": "power_consumption_per_year_after_conversion_in_kwh", "label": _("Annual Power Consumption After (kWh)"), "fieldtype": "Float", "width": 120},
    ]
    return columns

def get_data(filters):
    conditions, filter_values = get_conditions(filters)
    
    query = """
        SELECT
            led.customer,
            led.customer_name,
            led.date,
            led.name AS transaction_id,
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
        FROM `tabLED Conversion Proposal` led
        JOIN `tabLED Conversion Proposal Details` ledt ON led.name = ledt.parent
        WHERE 1=1 {conditions}
        ORDER BY led.date, led.customer ASC
    """.format(conditions=conditions)

    return frappe.db.sql(query, filter_values, as_dict=True)

def get_conditions(filters):
    conditions = []
    filter_values = {}

    if filters.get("customer"):
        conditions.append("AND led.customer = %(customer)s")
        filter_values["customer"] = filters["customer"]

    if filters.get("transaction_id"):
        conditions.append("AND led.name = %(transaction_id)s")
        filter_values["transaction_id"] = filters["transaction_id"]

    if filters.get("from_date"):
        conditions.append("AND led.date >= %(from_date)s")
        filter_values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("AND led.date <= %(to_date)s")
        filter_values["to_date"] = filters["to_date"]

    return " ".join(conditions), filter_values
