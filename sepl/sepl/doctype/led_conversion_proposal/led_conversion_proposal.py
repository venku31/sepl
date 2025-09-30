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

    # 🔎 Check if all items have item_code
    missing_items = [row.idx for row in proposal_doc.proposal_detals if not row.item_code]
    if missing_items:
        frappe.throw(
            f"Item Code is missing in Proposal Details row(s): {', '.join(map(str, missing_items))}"
        )

    # ✅ Create Quotation
    quotation = frappe.new_doc("Quotation")
    quotation.quotation_to = "Customer"
    quotation.party_name = proposal_doc.customer
    quotation.transaction_date = nowdate()
    quotation.custom_vessel = proposal_doc.vessel  # if you have vessel field in Quotation

    for row in proposal_doc.proposal_detals:
        quotation.append("items", {
            "item_code": row.item_code,
            "qty": row.qty
        })

    quotation.insert(ignore_permissions=True, ignore_mandatory=True)
    frappe.db.commit()

    # 🔄 Update proposal with created quotation
    proposal_doc.db_set("quotation", quotation.name)   # quotation field in LED Conversion Proposal
    proposal_doc.reload()

    return quotation.name

