frappe.ui.form.on('Delivery Note', {
    refresh(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__('Link Sales Order'), () => {
                if (!frm.doc.customer) {
                    frappe.msgprint("Please select a Customer first.");
                    return;
                }

                frappe.db.get_list('Sales Order', {
                    filters: {
                        customer: frm.doc.customer,
                        docstatus: 1
                    },
                    fields: ['name']
                }).then(orders => {
                    if (orders.length === 0) {
                        frappe.msgprint("No submitted Sales Orders found for this customer.");
                        return;
                    }

                    let options = orders.map(order => order.name);

                    let d = new frappe.ui.Dialog({
                        title: 'Link Sales Order',
                        fields: [
                            {
                                label: 'Customer',
                                fieldname: 'customer',
                                fieldtype: 'Link',
                                options: 'Customer',
                                default: frm.doc.customer,
                                read_only: 1
                            },
                            {
                                label: 'Sales Order',
                                fieldname: 'sales_order',
                                fieldtype: 'Select',
                                options: options.join('\n'),
                                reqd: 1
                            }
                        ],
                        primary_action_label: 'Link',
                        primary_action(values) {
                            // Fetch Sales Order Items
                            frappe.db.get_doc('Sales Order', values.sales_order)
                                .then(so => {
                                    let so_items = so.items;

                                    frm.doc.items.forEach(dn_item => {
                                        // Try to find matching SO Item by item_code and qty
                                        let matching_so_item = so_items.find(so_item => 
                                            so_item.item_code === dn_item.item_code &&
                                            so_item.qty >= dn_item.qty // allow partial delivery
                                        );

                                        if (matching_so_item) {
                                            frappe.model.set_value(dn_item.doctype, dn_item.name, 'against_sales_order', values.sales_order);
                                            frappe.model.set_value(dn_item.doctype, dn_item.name, 'so_detail', matching_so_item.name);
                                        }
                                    });

                                    frm.refresh_field('items');
                                    d.hide();
                                    frappe.msgprint(`Linked Sales Order ${values.sales_order} to matching items.`);
                                });
                        }
                    });

                    d.show();
                });
            });
        }
    }
});
