// Copyright (c) 2024, SEPL and contributors
// For license information, please see license.txt

frappe.query_reports["Quotation Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ["",'Draft','Open','Replied','Partially Ordered','Ordered','Lost','Cancelled','Expired'],
			
	}
		
		
	],
	// "formatter": function (value, row, column, data, default_formatter) {
	// 	value = default_formatter(value, row, column, data);

	// 	if (column.fieldname.includes(__("status"))) {

	// 		if (data[column.fieldname] == "Draft") {
	// 			value = "<span style='color:red'>" + value + "</span>";
	// 		}
	// 		else if (data[column.fieldname] == "Open") {
	// 			value = "<span style='color:red'>" + value + "</span>";
	// 		}
	// 		else if (data[column.fieldname] == "Replied") {
	// 			value = "<span style='color:red'>" + value + "</span>";
	// 		}
	// 		else if (data[column.fieldname] == "Partially Ordered") {
	// 			value = "<span style='color:yellow'>" + value + "</span>";
	// 		}
	// 		else if (data[column.fieldname] == "Ordered") {
	// 			value = "<span style='color:green'>" + value + "</span>";
	// 		}
	// 		else if (data[column.fieldname] == "Lost") {
	// 			value = "<span style='color:pink'>" + value + "</span>";
	// 		}
	// 		else  {
	// 			value = "<span style='color:red'>" + value + "</span>";
	// 		}
	// 	}

	// 	return value;
	// }
};
