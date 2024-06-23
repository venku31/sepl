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
        main_total_qty(frm, cdt, cdn);
        },
})

// frappe.ui.form.on('LED Conversion Proposal Details', {
//         installed_bf_power_conversion: function(frm, cdt, cdn) {
//                 main_total_qty(frm, cdt, cdn);
//         }
// })

function main_total_qty(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var installed_bf_power_conversion = 0;
        frm.doc.proposal_detals.forEach(function(d) { installed_bf_power_conversion += d.installed_bf_power_conversion});
        frm.set_value('installed_bf_power_conversion', installed_bf_power_conversion);

        var power_before_conversion_at_sea = 0;
        frm.doc.proposal_detals.forEach(function(d) { power_before_conversion_at_sea += d.power_before_conversion_at_sea});
        frm.set_value('power_before_conversion_at_sea', power_before_conversion_at_sea);

        var power_before_conversion_at_port = 0;
        frm.doc.proposal_detals.forEach(function(d) { power_before_conversion_at_port += d.power_before_conversion_at_port});
        frm.set_value('power_before_conversion_at_port', power_before_conversion_at_port);

        var installed_power_af_conversion = 0;
        frm.doc.proposal_detals.forEach(function(d) { installed_power_af_conversion += d.installed_power_af_conversion});
        frm.set_value('installed_power_af_conversion', installed_power_af_conversion);

        var power_after_conversion_at_sea = 0;
        frm.doc.proposal_detals.forEach(function(d) { power_after_conversion_at_sea += d.power_after_conversion_at_sea});
        frm.set_value('power_after_conversion_at_sea', power_after_conversion_at_sea);

        var power_after_conversion_at_port = 0;
        frm.doc.proposal_detals.forEach(function(d) { power_after_conversion_at_port += d.power_after_conversion_at_port});
        frm.set_value('power_after_conversion_at_port', power_after_conversion_at_port);

        var power_consumption_per_year_before_conversion_in_kwh = 0;
        frm.doc.proposal_detals.forEach(function(d) { power_consumption_per_year_before_conversion_in_kwh += d.power_consumption_per_year_before_conversion_in_kwh});
        frm.set_value('power_consumption_per_year_before_conversion_in_kwh', power_consumption_per_year_before_conversion_in_kwh);

        var power_consumption_per_year_after_conversion_in_kwh = 0;
        frm.doc.proposal_detals.forEach(function(d) { power_consumption_per_year_after_conversion_in_kwh += d.power_consumption_per_year_after_conversion_in_kwh});
        frm.set_value('power_consumption_per_year_after_conversion_in_kwh', power_consumption_per_year_after_conversion_in_kwh);
        frm.set_value('power_savings', power_consumption_per_year_before_conversion_in_kwh-power_consumption_per_year_after_conversion_in_kwh);
        frm.set_value('power_saving_per_year', power_after_conversion_at_port);
        frm.set_value('fuel_saving_per_year', power_after_conversion_at_port*220/1000000);
        frm.set_value('fuel_cost_saving__per_year', frm.doc.fuel_saving_per_year*650);
        frm.set_value('co2_saving_per_year', frm.doc.fuel_saving_per_year*3.5);
        }	