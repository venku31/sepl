# Copyright (c) 2024, SEPL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class LEDConversionProposal(Document):
	pass


@frappe.whitelist()
def create_quotation(proposal):
    proposal_doc = frappe.get_doc("LED Conversion Proposal", proposal)

    if not proposal_doc.customer:
        frappe.throw("Customer is mandatory")

    # Create Quotation
    quotation = frappe.new_doc("Quotation")
    quotation.quotation_to = "Customer"
    quotation.party_name = proposal_doc.customer
    quotation.transaction_date = nowdate()
    quotation.custom_vessel = proposal_doc.vessel  # if you have vessel field in Quotation

    for row in proposal_doc.proposal_detals:
        item_code = row.sepl_proposal

        # Check if Item exists
        if not frappe.db.exists("Item", item_code):
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": item_code,
                "item_name": item_code,
                "item_group": "Products",   # change as per your setup
                "stock_uom": "Nos",        # default UOM
                "is_sales_item": 1
            })
            item.insert(ignore_permissions=True, ignore_mandatory=True)
            frappe.db.commit()

        # Add item to quotation
        quotation.append("items", {
            "item_code": item_code,
            "qty": row.qty
        })

    quotation.insert(ignore_permissions=True, ignore_mandatory=True)
    frappe.db.commit()

    return quotation.name
