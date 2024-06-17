// frappe.ui.form.on('LED Conversion Proposal', {
// 	refresh(frm) {
		
// 	}
// })
frappe.ui.form.on('LED Conversion Proposal', {
	validate: function(frm, cdt, cdn){ 
        var d = locals[cdt][cdn];
        // d.installed_bf_power_conversion = d.units+d.wattage;
        frm.doc.proposal_detals.forEach(function(d) { 
                d.installed_bf_power_conversion = d.units*d.wattage;
                d.power_before_conversion_at_port = (d.units*d.wattage)*d.usage_factor*0.4;
                d.installed_power_af_conversion = d.sepl_wattage*d.qty;
                d.power_after_conversion_at_port = (d.sepl_wattage*d.qty)*d.usage_factor*0.4;
                d.power_consumption_per_year_before_conversion_in_kwh = ((d.power_before_conversion_at_sea+((d.units*d.wattage)*d.usage_factor*0.4)))*24*365/1000;
                d.power_consumption_per_year_after_conversion_in_kwh = ((d.power_after_conversion_at_sea+((d.sepl_wattage*d.qty)*d.usage_factor*0.4)))*24*365/1000
        });
        },
})