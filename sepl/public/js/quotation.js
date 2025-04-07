frappe.ui.form.on('Quotation', {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Delivery Note'), () => {
            frappe.call({
    method: "sepl.api.delivery_note.create_delivery_note_from_quotation",
    args: {
        quotation_name: frm.doc.name
    },
    callback: function(r) {
        if (!r.exc && r.message) {
            frappe.model.sync(r.message);
            frappe.set_route("Form", r.message.doctype, r.message.name);
        } else {
            frappe.msgprint("Failed to create Delivery Note.");
        }
    }
});


            }, __('Create'));
        }
    }
});