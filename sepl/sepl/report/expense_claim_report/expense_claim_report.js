// Copyright (c) 2025, SEPL and contributors
// For license information, please see license.txt

// frappe.query_reports["Expense Claim Report"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Expense Claim Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        }
    ]
};
