// Copyright (c) 2024, SEPL and contributors
// For license information, please see license.txt

frappe.query_reports["LED Conversion Proposal"] = {
	"filters": [
		{
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "width": "80",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "width": "80",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },

		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"transaction_id",
			"label": __("ID"),
			"fieldtype": "Link",
			"options": "LED Conversion Proposal"
			
	}
		
		
	],
};
