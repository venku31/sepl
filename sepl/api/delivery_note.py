import frappe

@frappe.whitelist()
def create_delivery_note_from_quotation(quotation_name):
    quotation = frappe.get_doc("Quotation", quotation_name)
    delivery_note = frappe.new_doc("Delivery Note")

    if quotation.quotation_to != "Customer":
        frappe.throw("Quotation is not for a Customer. Cannot create Delivery Note.")

    delivery_note.customer = quotation.party_name
    delivery_note.quotation = quotation.name
    delivery_note.set_posting_time = 1
    delivery_note.posting_date = frappe.utils.nowdate()

    for item in quotation.items:
        delivery_note.append("items", {
            "item_code": item.item_code,
            "item_name": item.item_name,
            "description": item.description,
            "qty": item.qty,
            "uom": item.uom,
            "rate": item.rate,
            "conversion_factor": item.conversion_factor,
            "warehouse": item.warehouse or "Stores - W",
            "quotation_item": item.name,
            "against_quotation" :quotation.name
        })

    delivery_note.insert(ignore_permissions=True)
    delivery_note.reload()
    return delivery_note.as_dict()
