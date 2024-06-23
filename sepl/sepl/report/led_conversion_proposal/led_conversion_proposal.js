// Copyright (c) 2024, SEPL and contributors
// For license information, please see license.txt

frappe.query_reports["LED Conversion Proposal"] = {
	"filters": [

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
